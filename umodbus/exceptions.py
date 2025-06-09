from typing import Dict

MODBUS_OP_CODES: Dict[int, str] = {
    1: 'Read Coils (1)',
    2: 'Read Discrete Inputs (2)',
    3: 'Read Holding Registers (3)',
    4: 'Read Input Registers (4)',
    5: 'Write Single Coil (5)',
    6: 'Write Single Register (6)',
    7: 'Read Exception Status (7)',
    8: 'Diagnostics (8)',
    15: 'Write Multiple Coils (15)',
    16: 'Write Multiple Registers (16)',
    20: 'Read File Record (20)',
    21: 'Write File Record (21)',
    22: 'Mask Write Register (22)',
    23: 'Read/Write Multiple Registers (23)',
    24: 'Read FIFO (24)'
}


class ModbusError(Exception):
    """ Base class for all Modbus related exception. """

    def __init__(self, payload: bytes):
        self._payload = payload

    @property
    def modbus_op_code(self) -> str:
        """
        Retrieves the Modbus operation code from the payload and returns a corresponding
        description.

        This property extracts the Modbus function code from the payload, adjusts it to account for
        the error response offset (0x80), and then maps it to a human-readable description using
        the MODBUS_OP_CODES dictionary.

        Returns
        -------
        str
            A string representing the Modbus function code. The possible return values are:
            - 'Read Coils (1)'
            - 'Read Discrete Inputs (2)'
            - 'Read Holding Registers (3)'
            - 'Read Input Registers (4)'
            - 'Write Single Coil (5)'
            - 'Write Single Register (6)'
            - 'Read Exception Status (7)'
            - 'Diagnostics (8)'
            - 'Write Multiple Coils (15)'
            - 'Write Multiple Registers (16)'
            - 'Read File Record (20)'
            - 'Write File Record (21)'
            - 'Mask Write Register (22)'
            - 'Read/Write Multiple Registers (23)'
            - 'Read FIFO (24)'

            If the function code is not recognized, it returns a string in the format
            "Unknown Opcode: <opcode>".

        Raises
        ------
        KeyError
            If the Modbus function code is not found in the MODBUS_OP_CODES dictionary.
        """
        opcode = int(self._payload[0]) - int(0x80)

        try:
            return MODBUS_OP_CODES[opcode]
        except KeyError:
            return f"Unknown Opcode: {opcode}"


class IllegalFunctionError(ModbusError):
    """ The function code received in the request is not an allowable action for
    the server.

    """
    error_code = 1

    def __str__(self):
        return 'Function code is not an allowable action for the server.'


class IllegalDataAddressError(ModbusError):
    """ The data address received in the request is not an allowable address for
    the server.
    """
    error_code = 2

    def __str__(self):
        return self.__doc__


class IllegalDataValueError(ModbusError):
    """ The value contained in the request data field is not an allowable value
    for the server.

    """
    error_code = 3

    def __str__(self):
        return self.__doc__


class ServerDeviceFailureError(ModbusError):
    """ An unrecoverable error occurred. """
    error_code = 4

    def __str__(self):
        return 'An unrecoverable error occurred.'


class AcknowledgeError(ModbusError):
    """ The server has accepted the requests and it processing it, but a long
    duration of time will be required to do so.
    """
    error_code = 5

    def __str__(self):
        return self.__doc__


class ServerDeviceBusyError(ModbusError):
    """ The server is engaged in a long-duration program command. """
    error_code = 6

    def __str__(self):
        return self.__doc__


class MemoryParityError(ModbusError):
    """ The server attempted to read record file, but detected a parity error
    in memory.

    """
    error_code = 8

    def __repr__(self):
        return self.__doc__


class GatewayPathUnavailableError(ModbusError):
    """ The gateway is probably misconfigured or overloaded. """
    error_code = 10

    def __repr__(self):
        return self.__doc__


class GatewayTargetDeviceFailedToRespondError(ModbusError):
    """ Didn't get a response from target device. """
    error_code = 11

    def __repr__(self):
        return self.__doc__

error_code_to_exception_map = {
    IllegalFunctionError.error_code: IllegalFunctionError,
    IllegalDataAddressError.error_code: IllegalDataAddressError,
    IllegalDataValueError.error_code: IllegalDataValueError,
    ServerDeviceFailureError.error_code: ServerDeviceFailureError,
    AcknowledgeError.error_code: AcknowledgeError,
    ServerDeviceBusyError.error_code: ServerDeviceBusyError,
    MemoryParityError.error_code: MemoryParityError,
    GatewayPathUnavailableError.error_code: GatewayPathUnavailableError,
    GatewayTargetDeviceFailedToRespondError.error_code:
        GatewayTargetDeviceFailedToRespondError
}
