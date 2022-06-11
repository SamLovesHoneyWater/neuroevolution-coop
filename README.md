# Universal Representations among RNN Agents
## About

This is a project that explores the universality of vector representations among RNNs.
RNNs that are trained independently to play a game have a high chance of being able to understand each other's vector representations of game information, even without previous encounters.

## The Experiment

Using neuroevolution, RNNs are trained to play modified versions of the game Pong, independently.
At one phase during training, game information is periodically hidden from RNN agents, forcing them to develop representations of game information in their recurrent units.
Then, when agents without common ancestry are put together to perform a cooperative task, they have a high chance of demonstrating behaviors that indicate they can understand each other’s representations of game information. 
This repo also contains codes for control experiments that can confirm the significance of this result.

## The Cooperation Task

There are two agents in the cooperative task. The first agent, the “speaker”, is always able to receive full game input, but it cannot move the bat. Its task is merely to produce recurrent signals according to the inputs, which are then sent to the second agent. The second agent is the “actor”. It cannot observe game inputs, but has to move the bat according to the recurrent signals sent by the first agent. Specifically, its recurrent inputs are set to the values of the first agent’s recurrent outputs, and its own outputs are realized into bat movement in the game.
Intuitively, the “actor” cannot see and has to act on what the “speaker” tells it. Note that they are not trained to cooperate at all, and that they do not have common training ancestry.

## My Results

I generated 21 agents. In a round robin test, out of 420 rounds, 20% are able to perform well enough to reach a certain threshold score. I.e., in 20% of the cases, the "actor" is able to generate sufficiently correct game outputs according to representations given by another agent, the "speaker".

## Try It

get_coop_agents.py provides a streamlined way to produce families of RNNs for future testing in a cooperative task.
compare_coop_agents.py provides functions to evaluate and clean families, select one from each family, and test them on how well they understand each other's vector representations of game information.
single_agent_evolution.py can be used to produce a family of RNNs to play the unmodified version of Pong.
