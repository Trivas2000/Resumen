package com.example.aventurasdemarcoyluis.model.game.patterns.phases;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * The first Phase of a character turn in the game, it takes starts with players because marco always plays first
 */
public class NewTurnPhase extends StandardPhase{

    /***
     * Transitions to start of player turn phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToPlayerStartOfTurnPhase(){
        simulator.setPhase(new StartOfPlayerTurnWaitPhase());
    }

}
