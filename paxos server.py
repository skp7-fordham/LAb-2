import grpc
from concurrent import futures
import time
import paxos_pb2
import paxos_pb2_grpc

class PaxosNode(paxos_pb2_grpc.PaxosServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.current_proposal_number = 0
        self.accepted_proposal = None

    def Prepare(self, request, context):
        print(f"Node {self.node_id} received Prepare request for proposal {request.proposal_number}")
        if request.proposal_number > self.current_proposal_number:
            self.current_proposal_number = request.proposal_number
            return paxos_pb2.PrepareResponse(success=True)
        return paxos_pb2.PrepareResponse(success=False)

    def Accept(self, request, context):
        print(f"Node {self.node_id} received Accept request for proposal {request.proposal_number}")
        if self.accepted_proposal is None or self.accepted_proposal[0] < request.proposal_number:
            self.accepted_proposal = (request.proposal_number, request.value)
            return paxos_pb2.AcceptResponse(success=True)
        return paxos_pb2.AcceptResponse(success=False)

    def Propose(self, request, context):
        print(f"Node {self.node_id} received Propose request for proposal {request.proposal_number}")
        # Simulate the Prepare and Accept phases
        success = self.prepare_proposal(request.proposal_number)
        if success:
            success = self.accept_proposal(request.proposal_number, request.value)
        return paxos_pb2.ProposeResponse(success=success)

    def prepare_proposal(self, proposal_number):
        print(f"Node {self.node_id} preparing proposal {proposal_number}")
        return True

    def accept_proposal(self, proposal_number, value):
        print(f"Node {self.node_id} accepting proposal {proposal_number} with value {value}")
        return True

        def serve(node_id, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    paxos_node = PaxosNode(node_id)
    paxos_pb2_grpc.add_PaxosServicer_to_server(paxos_node, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Node {node_id} listening on port {port}...")
    server.wait_for_termination()

if __name__ == '__main__':
    
    serve(3, 50053) 