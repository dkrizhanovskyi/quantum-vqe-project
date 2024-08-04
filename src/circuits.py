import pennylane as qml

def create_vqe_circuit(params, circuit_type='default'):
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
