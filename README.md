# README

## Video

Demonstration video link: `https://drive.google.com/file/d/1o6yETIxo-DPrrXYDx3pdObF5TCW5yvF-/view'

## Run

From the project root, run:

```bash
python Evaluation.py
```

If needed, use:

```bash
python3 Evaluation.py
```

## Reproduce The Experiments

- Random seed: `42`
- Minimax depth: `4`
- Pairings:
  - Random vs Rule-Based
  - Rule-Based vs Minimax
  - Minimax vs Random
- Each pairing runs `30` games
- The starting player alternates after `15` games

The seed is set in `Evaluation.py` with:

```python
random.seed(42)
```
