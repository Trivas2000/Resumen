package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * The phase of the start of a players turn
 */
public class StartOfPlayerTurnWaitPhase extends StandardPhase{

    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    @Override
    public String toString(){return "Start of player turn Phase";}


    /***
     * Transitions to choosing attack  phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToChoosingAttackPhase()throws InvalidPhaseTransitionException {
        setPhase(new PlayerChoosesAttackTypeWaitingPhase());
    }


    /***
     * Transitions to choosing item phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToChoosingItemPhase()throws InvalidPhaseTransitionException {
        setPhase(new PlayerChooseItemWaitingPhase());
    }


    /***
     * Transitions to pass turn phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToPassTurnPhase() throws InvalidPhaseTransitionException, InvalidActionException {
        setPhase(new PlayerPassTurnPhase());

    }

}
