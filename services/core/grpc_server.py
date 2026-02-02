from concurrent import futures
import grpc
import logging
# These imports will work after proto generation
import protos.delivery_pb2 as pb2
import protos.delivery_pb2_grpc as pb2_grpc

class DeliveryService(pb2_grpc.DeliveryServiceServicer):
    def CalculatePrice(self, request, context):
        price = request.distance_km * 5.0
        if request.is_express:
            price *= 1.5
        
        return pb2.DeliveryResponse(
            price=price, 
            estimated_time="2h" if request.is_express else "24h"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_DeliveryServiceServicer_to_server(DeliveryService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
