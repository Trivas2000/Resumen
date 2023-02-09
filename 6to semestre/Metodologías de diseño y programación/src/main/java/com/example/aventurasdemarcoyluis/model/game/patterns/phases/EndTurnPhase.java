package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase where the turn of the current character ends
 */
public class EndTurnPhase extends StandardPhase {



    /***
     * Transitions to start of player turn phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToPlayerStartOfTurnPhase() {
        simulator.setPhase(new StartOfPlayerTurnWaitPhase());
    }

    /***
     * Transitions to choose enemy target phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionEnemyToChooseTargetPhase() {
        simulator.setPhase(new EnemyChooseTargetPhase());
    }


    /**
     Method for ending the turn and starting the next one phase
     */
    @Override
    public void endTurn() throws InvalidPhaseTransitionException, InvalidActionException {
        simulator.advanceTurn();
        if(simulator.checkIfCurrentTurnOwnerIsPlayer()){
            transitionToPlayerStartOfTurnPhase();
        }
        else{
            transitionEnemyToChooseTargetPhase();
            simulator.getPhase().chooseEnemyTarget();}

    }
}
