import pennylane as qml
from typing import Callable, List

def create_vqe_circuit(params: List[float], circuit_type: str = 'default') -> Callable:
    """
    Create a Variational Quantum Eigensolver (VQE) circuit based on the specified type.

    Args:
        params: A list of float numbers representing the parameters for the quantum gates.
        circuit_type: A string indicating the type of the circuit ('default' or 'alternate').

    Returns:
        A callable quantum node (QNode) representing the VQE circuit.

    Raises:
        ValueError: If the specified circuit type is unknown.
    """
    dev = qml.device('default.qubit', wires=2)

    @qml.qnode(dev)
    def default_circuit():
        qml.RX(params[0], wires=0)
        qml.RY(params[1], wires=1)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.PauliZ(0))

    @qml.qnode(dev)
    def alternate_circuit():
        qml.Hadamard(wires=0)
        qml.CRX(params[0], wires=[0, 1])
        qml.RY(params[1], wires=1)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.PauliZ(0))

    if circuit_type == 'default':
        return default_circuit
    elif circuit_type == 'alternate':
        return alternate_circuit
    else:
        raise ValueError("Unknown circuit type")
