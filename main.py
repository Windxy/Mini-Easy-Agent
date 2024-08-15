from brain.Agent import Agent

# lmdeploy serve api_server Qwen/Qwen2-7B-Instruct --server-port 23333
def main():
    agent = Agent()
    agent.enter()

if __name__ == "__main__":
    main()