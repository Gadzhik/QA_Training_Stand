import multiprocessing
import uvicorn
import services.core.grpc_server as grpc_srv

def run_rest():
    uvicorn.run("services.core.main:app", host="0.0.0.0", port=8000, reload=False)

def run_grpc():
    grpc_srv.serve()

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_rest)
    p2 = multiprocessing.Process(target=run_grpc)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
