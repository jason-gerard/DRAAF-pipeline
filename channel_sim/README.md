# Channel Sim

Channel sim is a Monte Carlo simulator built to compare different channel coding methods. It uses the LoRa physical layer and a channel with a single transmitter, an IoT node, and a single receiver, a LEO satellite. Channel sim allows decoupling the MAC protocol and the channel coding method to better test it at different BER. The number of repetitions of the Monte Carlo simulation can be adjusted to improve convergence.

In satellite communications the channels are often collision channels without feedback meaning error detection isn't very useful because we have no way easily alert the IoT node on the ground. This means that the primary way to account for error is FEC with channel coding. In general LEO satellites and ground nodes have low BER channels meaning this isn't a large issue, but when moving to different planets like Mars during a dust storm or out of LEO and getting further away from the ground devices, the BER can increase.

### TODO
- Update energy model to include decoding energy consumption based on Big O complexity
- Add actual channel models instead of hard coded BERs
  - Earth, baseline 10^-9
  - Mars
  - Moon, might just be some free space link BER in a vacuum