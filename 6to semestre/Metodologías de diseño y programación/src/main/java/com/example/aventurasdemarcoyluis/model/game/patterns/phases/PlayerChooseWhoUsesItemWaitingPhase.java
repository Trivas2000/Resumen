package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase for choosing the player that uses the item
 */
public class PlayerChooseWhoUsesItemWaitingPhase extends StandardPhase{
    int itemIndex;
    int playerIndex;
    public PlayerChooseWhoUsesItemWaitingPhase(int itemIndex) {
        this.itemIndex=itemIndex;
    }


    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    @Override
    public String toString(){return "Player choose who uses item Phase";}


    /***
     * Transitions to use item phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToUsingItemPhase() throws InvalidPhaseTransitionException {
        simulator.setPhase(new UseItemPhase(itemIndex,playerIndex));
    }


    /***
     * Method for choosing a player and advancing to the next phase
     * @param newPlayerIndex the index of the player we choose
     * @throws InvalidPhaseTransitionException when you can not transition
     * @throws InvalidActionException when you can not perform an action
     */
    @Override
    public void choosePlayer(int newPlayerIndex)throws InvalidPhaseTransitionException, InvalidActionException {
        this.playerIndex=newPlayerIndex;
        transitionToUsingItemPhase();
    }
}
