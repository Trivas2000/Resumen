package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase where the enemy attacks
 */
public class EnemyAttackPhase extends StandardPhase{
    private int playerIndex;
    public EnemyAttackPhase(int playerIndex) {
        this.playerIndex=playerIndex;

    }




    /**
     Transitions to end turn phase
     @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToEndTurnPhase() {
        setPhase(new EndTurnPhase());
    }


    /**
     Method for enemy attack
     */
    @Override
    public void enemyPhaseAttack() throws InvalidPhaseTransitionException, InvalidActionException {
        simulator.enemyAttack(playerIndex);
        transitionToEndTurnPhase();
        simulator.getPhase().endTurn();
    }
}
