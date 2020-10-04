"""
Utilties for files transfer over networks.
"""

import socket
import logging

import paramiko
import scp
import re

import credentials

def generate_ip_list(ip_base):
    """
    A dirty fill in for a CIDR mask, just to handle the possibility of
    either a search over a range of IPs, or just a single IP, in SCP transfer.

    Parameters
    ----------
    ip_base : str
        Partial or full specification of an IP address. Only handles
        where first three numbers or all four are specified.

    Returns
    -------
    ip_list : list
        List of potential IP addresses matching the base input. If a range,
        will be 1 to 254.

    Examples
    --------
    >>> from improc.gen import transfer
    >>> print(transfer.generate_ip_list("192.168.1.1"))
    ['192.168.1.1']
    >>> print(transfer.generate_ip_list("192.168.1.")[:5])
    ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5']
    """

    ip_base_split = ip_base.split(".")
    ip_base_nums = [ip_num for ip_num in ip_base_split if ip_num != ""]
    if len(ip_base_nums) == 4:
        return [".".join(ip_base_nums)]
    elif len(ip_base_nums) == 3:
        possibilities = map(str, range(1, 255))
        return [".".join(ip_base_nums + [p]) for p in possibilities]


def guess_system_ip(ip_base="192.168.1.", system=data_acq,
                    system_name="weather1"):
    """
    Looks over a network for a system that can be logged into via SSH
    with the provided credentials. If it finds a system, returns the IP
    address. For dealing with data acq systems that have unknown address.

    Parameters
    ----------
    ip_base : str (opt)
        Partial or full specification of an IP address. Only handles
        where first three numbers or all four are specified. Default
        is 192.168.1, which is a common local network.
    system : dict (opt)
        A dictionary with keys "user", "password", and "ports", in
        which "ports" is itself a dict with key "ssh".
    system_name : str (opt)
        If specified, will only return ip address matching system_name

    Returns
    -------
    ip_guess : str
        Guess for IP of system, based on being able to log in via SSH. If
        not found, returns None.
    """

    # setup for dumb search over local IP for the data acq system
    ips_to_try = generate_ip_list(ip_base)

    # continue looking on local network for a data acq system to connect to
    # until finally have success. not currently set with a static value,
    # so search the whole local network for something ssh-able
    success = False
    while not success:
        for ip_guess in ips_to_try:
            try:
                print("Trying " + ip_guess)
                # try to connect to the IP address. If you connect and the system name matches the hostname,
                # return the IP address. Otherwise continue.
                if _check_system_name(ip_guess, system_name, system):
                    return ip_guess
                else:
                    continue

            except (TimeoutError, socket.timeout,
                    paramiko.ssh_exception.SSHException,
                    paramiko.ssh_exception.NoValidConnectionsError,
                    paramiko.ssh_exception.AuthenticationException):
                # TODO: catching AuthenticationException is dangerous; we might
                #       never realize we're using the wrong credentials. it is
                #       here because there are other users on the local
                #       network.

                continue
        osops.safe_sleep(10)


def _check_system_name(ip_address, system_name, system=data_acq):
    """
    Check that the provided system name and the hostname of the host at the provided IP address are
    consistent.

    Parameters
    ----------
    ip_address : str
    system_name : str
    system

    Returns
    -------
    bool
        True when provided system_name matches the hostname at the IP address.

    Raises
    ------
    exception when no connection to the host is available.
    """

    ssh_client = create_ssh_client(
        ip_address=ip_address,
        port=system["ports"]["ssh"],
        user=system["user"],
        password=system["password"])

    if system_name:
        _, stdout, _ = ssh_client.exec_command('hostname')
        hostname = stdout.read()
        if isinstance(hostname, bytes):
            hostname = hostname.decode('utf-8')
    ssh_client.close()

    if system_name:
        if sanitize_system_name(hostname) == sanitize_system_name(system_name):
            return True
        else:
            print('System name {} does not match hostname ({}) at IP {}.'.format(
                system_name, hostname, ip_address)
            )
            return False
    else:
        # You connected and don't know what your host name should be so, success(?)
        return True


def sanitize_system_name(system_name):
    """
    Return reasonably well formatted system names as:
    name+integer
    """
    system_name = system_name.lower().strip()
    sys_type = get_chars(system_name)
    sys_num = get_nums(system_name)
    if len(sys_num) > 0:
        sys_num = str(int(sys_num))
    return sys_type + sys_num


def get_chars(s):
    """
    Returns all characters from a string, as a string.

    Parameters
    ----------
    s : str
        The string to be searched.

    Returns
    -------
    chars : str
        Given string, with only characters remaining.

    Example
    -------
    >>> from improc.gen import strops
    >>> test_str = "123abc456def"
    >>> chars = strops.get_chars(test_str)
    >>> print(chars)
    abcdef
    """

    chars = "".join(re.findall("[a-zA-Z]+", s))

    return chars


def get_nums(s):
    """
    Returns all numbers from a string, as a string.

    Parameters
    ----------
    s : str
        The string to be searched.

    Returns
    -------
    chars : str
        Given string, with only characters remaining.

    Example
    -------
    >>> from improc.gen import strops
    >>> test_str = "123abc456def"
    >>> nums = strops.get_nums(test_str)
    >>> print(nums)
    123456
    """

    nums = "".join(re.findall("[0-9]+", s))

    return nums

###############################################################################
# SSH/SCP


def create_ssh_client(ip_address, port, user, password):
    """Configure basic ssh client."""

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip_address, port, user, password, timeout=1)

    return ssh_client


def create_scp_client(ssh_client):
    """
    Creates a client for SCP transfer, given an open SSH client.

    See `create_ssh_client` to create an SSH client.
    """

    # sanitize argument lets us pass wildcards to get calls
    scp_client = scp.SCPClient(ssh_client.get_transport(),
                               sanitize=lambda x: x, socket_timeout=1)

    return scp_client
