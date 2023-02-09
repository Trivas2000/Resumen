package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase where the player chooses the attack type
 */

public class PlayerChoosesAttackTypeWaitingPhase extends StandardPhase{
    public int attackIndex;

    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    @Override
    public String toString(){return "Choosing attack type Phase";}


    /***
     * Transitions to choosing enemy to attack phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToChoosingEnemyToAttackPhase() throws InvalidPhaseTransitionException {
        simulator.setPhase(new PlayerChooseEnemyToAttackWaitingPhase(attackIndex));
    }


    /***
     * Method for choosing attack type
     * @param attackIndex the index of the attack we choose
     * @throws InvalidPhaseTransitionException when you can not transition
     * @throws InvalidActionException when you can not do the action
     */
    @Override
    public void chooseAttackType(int attackIndex)throws InvalidPhaseTransitionException, InvalidActionException {
        this.attackIndex=attackIndex;
        transitionToChoosingEnemyToAttackPhase();
    }
}
