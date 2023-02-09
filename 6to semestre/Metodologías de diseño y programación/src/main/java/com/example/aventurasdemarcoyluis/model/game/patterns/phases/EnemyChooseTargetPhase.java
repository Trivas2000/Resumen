package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase where the enemy chooses its target
 */
public class EnemyChooseTargetPhase extends  StandardPhase{
    public int playerIndex;


    /**
     Transitions to end turn phase
     @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToEndTurnPhase() {
        setPhase(new EndTurnPhase());
    }


    /**
     Transitions to enemy attack phase
     @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToEnemyAttackPhase() {
        setPhase(new EnemyAttackPhase(playerIndex));
    }


    /**
     Method for choosing enemy target
     @throws InvalidPhaseTransitionException when you can not transition
      * @throws InvalidActionException when you can not do the action
     */
    @Override
    public void chooseEnemyTarget() throws InvalidPhaseTransitionException, InvalidActionException {
        if(simulator.checkIfCurrentTurnIsBoo() && simulator.isLuisKod()){
            transitionToEndTurnPhase();
            endTurn();
        }
        else if(simulator.checkIfCurrentTurnIsBoo() || simulator.isLuisKod()){
            playerIndex=1;
            transitionToEnemyAttackPhase();
            simulator.getPhase().enemyPhaseAttack();
        }
        else if(simulator.isMarcoKod()){
            playerIndex=2;
            transitionToEnemyAttackPhase();
            simulator.getPhase().enemyPhaseAttack();
        }
        else {
            int random=simulator.currentTurnCharacter().generateRandomInt(1,2);
            playerIndex=random;
            transitionToEnemyAttackPhase();
            simulator.getPhase().enemyPhaseAttack();
        }

    }
}
