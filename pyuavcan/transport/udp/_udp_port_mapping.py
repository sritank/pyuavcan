#
# Copyright (c) 2019 UAVCAN Development Team
# This software is distributed under the terms of the MIT License.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from pyuavcan.transport import DataSpecifier, MessageDataSpecifier, ServiceDataSpecifier


SUBJECT_ID_OFFSET = 16384


def map_data_specifier_to_udp_port_number(ds: DataSpecifier) -> int:
    """
    Maps the data specifier to the UDP port number.

    For subjects, the UDP port number equals the subject-ID plus 2**14=16384.
    The offset is chosen so that UAVCAN ports do not conflict with the IANA-reserved range for ephemeral ports
    and commonly-used lower port numbers.

    UDP port numbers for services grow downward from the same offset;
    even ports for requests, odd ports for responses.
    Services grow downward to allow for a possible future extension of the service-ID
    range without breaking the existing mapping.

    >>> map_data_specifier_to_udp_port_number(MessageDataSpecifier(0))
    16384
    >>> map_data_specifier_to_udp_port_number(MessageDataSpecifier(MessageDataSpecifier.SUBJECT_ID_MASK))
    49151
    >>> map_data_specifier_to_udp_port_number(ServiceDataSpecifier(0, ServiceDataSpecifier.Role.REQUEST))
    16382
    >>> map_data_specifier_to_udp_port_number(ServiceDataSpecifier(0, ServiceDataSpecifier.Role.RESPONSE))
    16383
    >>> map_data_specifier_to_udp_port_number(ServiceDataSpecifier(511, ServiceDataSpecifier.Role.REQUEST))
    15360
    >>> map_data_specifier_to_udp_port_number(ServiceDataSpecifier(511, ServiceDataSpecifier.Role.RESPONSE))
    15361
    """
    if isinstance(ds, MessageDataSpecifier):
        return ds.subject_id + SUBJECT_ID_OFFSET

    if isinstance(ds, ServiceDataSpecifier):
        request = SUBJECT_ID_OFFSET - 2 - ds.service_id * 2
        if ds.role == ServiceDataSpecifier.Role.REQUEST:
            return request
        if ds.role == ServiceDataSpecifier.Role.RESPONSE:
            return request + 1

    raise ValueError(f'Unsupported data specifier: {ds}')  # pragma: no cover
