package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase where we choose the enemy the player attacks
 */
public class PlayerChooseEnemyToAttackWaitingPhase extends StandardPhase{
    public int attackIndex;
    public PlayerChooseEnemyToAttackWaitingPhase(int attackIndex) {
        this.attackIndex=attackIndex;
    }


    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    @Override
    public String toString(){return "Player chooses enemy to attack Phase";}


    /***
     * Transitions to end turn phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToEndTurnPhase() {
        setPhase(new EndTurnPhase());
    }


    /***
     *Method for attacking an enemy and ending the turn
     */
    @Override
    public void phaseAttack(int enemyIndex) throws InvalidPhaseTransitionException {

        if (!simulator.checkIfCurrentTurnIsLuis()) {
            simulator.marcoAttack(enemyIndex, attackIndex);
        }
        else{
            simulator.luisAttack(enemyIndex,attackIndex);}
        transitionToEndTurnPhase();
    }
}
