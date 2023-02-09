package com.example.aventurasdemarcoyluis.model.game.patterns.phases;

import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;

/***
 * Phase where the item is used
 */
public class UseItemPhase extends StandardPhase{
    public int itemIndex;
    public int playerIndex;
    public UseItemPhase(int itemIndex,int playerIndex)  {
        this.itemIndex=itemIndex;
        this.playerIndex=playerIndex;


    }

    /***
     * Returns the name of the phase
     * @return the name of the phase
     */
    @Override
    public String toString(){return "Use item Phase";}


    /***
     * Transitions to end turn phase
     * @throws InvalidPhaseTransitionException when you can not transition
     */
    @Override
    public void transitionToEndTurnPhase()throws InvalidPhaseTransitionException {
        setPhase(new EndTurnPhase());
    }

    /***
     * Method for using item and transitioning to end phase
     */
    @Override
    public void useItem(){
        if (itemIndex==1){
            simulator.use("Red Mushroom",playerIndex);
        }
        else if(itemIndex==2){
            simulator.use("Honey Syrup",playerIndex);
        }
        try {
            transitionToEndTurnPhase();
        }catch (InvalidPhaseTransitionException e){
            e.printStackTrace();
        }
    }
}
