MOVE = bool
COOP = True
DEFECT = False
PAYOFF = {(COOP, COOP): (3, 3),
          (COOP, DEFECT): (0, 5),
          (DEFECT, COOP): (5, 0),
          (DEFECT, DEFECT): (1, 1)}
