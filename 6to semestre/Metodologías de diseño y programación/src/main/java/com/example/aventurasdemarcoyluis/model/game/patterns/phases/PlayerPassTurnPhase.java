package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * The phase where the player passes its turn
 */
public class PlayerPassTurnPhase extends StandardPhase{


    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    @Override
    public String toString(){return "Player pass turn Phase";}


    /***
     * Transitions to end turn phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToEndTurnPhase() throws InvalidPhaseTransitionException {
        simulator.setPhase(new EndTurnPhase());
    }


    /***
     * Player passes its turn
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void playerPassTurn() throws InvalidPhaseTransitionException, InvalidActionException {
        transitionToEndTurnPhase();

    }
}
