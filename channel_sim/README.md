# Channel Sim

Channel sim is a Monte Carlo simulator built to compare different channel coding methods. It uses the LoRa physical layer and a channel with a single transmitter, an IoT node, and a single receiver, a LEO satellite. Channel sim allows decoupling the MAC protocol and the channel coding method to better test it at different BER. The number of repititions of the Monte Carlo simulation can be adjusted to improve convergence.

In satellite communications the channels are often collision channels without feedback meaning error detection isn't very useful because we have no way easily alert the IoT node on the ground. This means that the primary way to account for error is FEC with channel coding. In general LEO satellites and ground nodes have low BER channels meaning this isn't a large issue, but when moving to different planets like Mars during a dust storm or out of LEO and getting further away from the ground devices, the BER can increase.

### TODO
- Add actual channel models instead of hard coded BERs
  - Earth
  - Mars
  - Moon
- Generate graphs from test runs
- Add more channel coding methods
- Right now a uniform BER is supported, in practice bursty BERs are much more common and so this is important to implement and test with