import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Main function for the Streamlit app
def main():
    st.title("Reverse English Auction Simulation")

    # User input for the number of suppliers
    num_suppliers = st.number_input("Enter the number of suppliers participating:", min_value=2, max_value=20, value=5)
    
    # Generate initial bids
    initial_bids = np.random.randint(800, 1000, size=num_suppliers)
    bids = {f"Supplier {i+1}": [bid] for i, bid in enumerate(initial_bids)}
    current_bids = initial_bids.copy()
    
    # Setting up the plot
    fig, ax = plt.subplots()
    ax.set_xlabel("Bid Round")
    ax.set_ylabel("Price")
    lines = [ax.plot([], [], label=f"Supplier {i+1}")[0] for i in range(num_suppliers)]
    ax.legend()
    
    # Placeholder for the graph
    graph_placeholder = st.empty()

    # Leaderboard placeholder
    leaderboard_placeholder = st.empty()

    # Timer and control
    if st.button("Start Auction"):
        countdown = 20
        timer_placeholder = st.empty()
        bid_round = 0
        while countdown > 0:
            time.sleep(1)
            countdown -= 1
            bid_round += 1
            timer_placeholder.markdown(f"Time Remaining: {countdown} seconds")

            # Simulate bidding
            for i in range(num_suppliers):
                if current_bids[i] > min(current_bids):
                    decrease = np.random.uniform(0.05, 0.3)
                    new_bid = current_bids[i] * (1 - decrease)
                    current_bids[i] = max(new_bid, min(current_bids) - np.random.uniform(1, 10))  # prevent bid < min bid
                    bids[f"Supplier {i+1}"].append(current_bids[i])
                else:
                    bids[f"Supplier {i+1}"].append(current_bids[i])

            # Update graph
            for line, bid_history in zip(lines, bids.values()):
                line.set_data(list(range(len(bid_history))), bid_history)
            ax.relim()
            ax.autoscale_view()
            graph_placeholder.pyplot(fig)
            
            # Update leaderboard
            sorted_bids = sorted((bid[-1], idx) for idx, bid in enumerate(bids.values()))
            leaderboard_data = {"Rank": range(1, len(sorted_bids[:5]) + 1),
                                "Supplier": [f"Supplier {idx+1}" for _, idx in sorted_bids[:5]],
                                "Bid": [bid for bid, _ in sorted_bids[:5]]}
            leaderboard_df = pd.DataFrame(leaderboard_data)
            leaderboard_placeholder.table(leaderboard_df)

        # Announce winner
        winner = sorted_bids[0][1]  # lowest bid
        st.success(f"Auction finished! Winner: Supplier {winner+1} with a bid of {sorted_bids[0][0]:.2f}")

if __name__ == "__main__":
    main()
