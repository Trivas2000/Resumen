package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.BattleSimulator;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * The base for all phases, it contains most methods throwing exceptions so that they are overridden in the child phases
 */
public class StandardPhase {
    protected BattleSimulator simulator;

    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    public String toString(){return "Standard Phase";}

    /***
     * Sets the controller of the phase
     * @param battleSimulator the controller
     */
    public void setController(BattleSimulator battleSimulator){this.simulator=battleSimulator;}

    /***
     * Sets a new phase for the controller
     * @param phase the new phase
     */
    protected void setPhase(StandardPhase phase) {simulator.setPhase(phase);}

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToPlayerStartOfTurnPhase()throws InvalidPhaseTransitionException {
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToChoosingAttackPhase()throws InvalidPhaseTransitionException {
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToChoosingEnemyToAttackPhase()throws InvalidPhaseTransitionException {
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToChoosingItemPhase() throws InvalidPhaseTransitionException{
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToUsingItemPhase() throws InvalidPhaseTransitionException{
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToChoosingPLayerWhoUsesItemPhase() throws InvalidPhaseTransitionException{
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToPassTurnPhase() throws InvalidPhaseTransitionException, InvalidActionException {
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToEndTurnPhase() throws InvalidPhaseTransitionException{
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionEnemyToChooseTargetPhase() throws InvalidPhaseTransitionException{
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToEnemyAttackPhase() throws InvalidPhaseTransitionException{
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Basic method for failed transition
     * @throws InvalidPhaseTransitionException when cannot transition
     */
    public void transitionToNewTurnPhase() throws InvalidPhaseTransitionException{
        throw new InvalidPhaseTransitionException("You can not do that right now");
    }

    /***
     * Method for choosing an item and advancing to the next phase
     * @param itemIndex the index of the item we choose
     * @throws InvalidPhaseTransitionException when you can not transition
     * @throws InvalidActionException when you can not perform an action
     */
    public void chooseItem(int itemIndex)throws InvalidPhaseTransitionException, InvalidActionException {
            throw new InvalidActionException("Yo can not perform that action");
    }

    /***
     * Method for choosing a player and advancing to the next phase
     * @param newPlayerIndex the index of the player we choose
     * @throws InvalidPhaseTransitionException when you can not transition
     * @throws InvalidActionException when you can not perform an action
     */
    public void choosePlayer(int newPlayerIndex)throws InvalidPhaseTransitionException, InvalidActionException {

            throw new InvalidActionException("You can not perform that action");
    }

    /***
     * Method for using item and transitioning to end phase
     * @throws InvalidActionException when you can not perform an action
     */
    public void useItem()throws InvalidActionException{
        throw new InvalidActionException("You can not perform that action");
    }

    /***
     * Player passes its turn
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    public void playerPassTurn() throws InvalidPhaseTransitionException,InvalidActionException{
        throw new InvalidActionException("You can not perform that action");
    }

    /***
     * Method for ending the turn and starting the next one phase
     */
    public void endTurn() throws InvalidPhaseTransitionException, InvalidActionException {
        throw new InvalidPhaseTransitionException("You can not do that right now");
        }

    /***
     *Method for attacking an enemy and ending the turn
     */
    public void phaseAttack(int enemyIndex) throws InvalidPhaseTransitionException,InvalidActionException {
        throw new InvalidActionException("You can not perform that action");

    }

    /***
     * Method for choosing attack type
     * @param attackIndex the index of the attack we choose
     * @throws InvalidPhaseTransitionException when you can not transition
     * @throws InvalidActionException when you can not do the action
     */
    public void chooseAttackType(int attackIndex)throws InvalidPhaseTransitionException, InvalidActionException {
        throw new InvalidActionException("You can not perform that action");
    }
    /***
     * Method for enemy attack
     */
    public void enemyPhaseAttack() throws InvalidActionException, InvalidPhaseTransitionException {
        throw new InvalidActionException("You can not perform that action");


    }

    /***
     * Method for choosing enemy target
     * @throws InvalidPhaseTransitionException when you can not transition
     * @throws InvalidActionException when you can not do the action
     */
    public void chooseEnemyTarget() throws InvalidPhaseTransitionException, InvalidActionException {
        throw new InvalidActionException("You can not perform that action");
    }

}

