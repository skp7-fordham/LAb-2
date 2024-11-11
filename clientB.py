import grpc
import paxos_pb2
import paxos_pb2_grpc
import time

# Function to send a propose request to the Paxos server
def send_propose_request(node_id, proposal_number, value):
    channel = grpc.insecure_channel('127.0.0.1:50053')  # Localhost IP, port 50053
    stub = paxos_pb2_grpc.PaxosStub(channel)

    # Create a ProposalRequest
    request = paxos_pb2.ProposalRequest(proposal_number=proposal_number, value=value, node_id=node_id)

    try:
        response = stub.Propose(request)
        print(f"Proposer {node_id}: Response from Node {node_id}: {response.success}")
    except grpc.RpcError as e:
        print(f"Proposer {node_id}: Error: {e.code()}, {e.details()}")

# Simulate the scenario where Proposer B wins (A's proposal is rejected)
def simulate_scenario_b():
    print("Proposer A sending proposal...")
    send_propose_request(node_id=1, proposal_number=1, value="value_A")
    
    # Simulate a scenario where Proposer A's proposal is rejected
    time.sleep(2)
    
    print("Proposer B sending proposal after Proposer A (higher proposal number)...")
    send_propose_request(node_id=2, proposal_number=2, value="value_B")

# Call the simulation function for Scenario B
simulate_scenario_b()