package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase where the player chooses the item to use
 */
public class PlayerChooseItemWaitingPhase extends StandardPhase{
    public int itemIndex;


    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    @Override
    public String toString(){return "Player choose item Phase";}



    /***
     * Transitions to choosing player who uses item phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToChoosingPLayerWhoUsesItemPhase() throws InvalidPhaseTransitionException {
        simulator.setPhase(new PlayerChooseWhoUsesItemWaitingPhase(itemIndex));
    }


    /***
     * Method for choosing an item and advancing to the next phase
     * @param itemIndex the index of the item we choose
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void chooseItem(int itemIndex)throws InvalidPhaseTransitionException, InvalidActionException {
        this.itemIndex=itemIndex;
        transitionToChoosingPLayerWhoUsesItemPhase();
    }
}
