package com.example.aventurasdemarcoyluis.model.characters.AbstractClasses;

import com.example.aventurasdemarcoyluis.model.characters.interfaces.Enemies;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;
import com.example.aventurasdemarcoyluis.model.items.Arsenal;
/***
 * This class represents the common ground for all the players in the game
 */
public abstract class AbstractPlayers extends AbstractCharacter implements Players {

    private int fp;
    private int maxFp;
    private Arsenal vault;

    /***

     * The constructor also makes a default arsenal for the player
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param MaxHp amount of hit points
     * @param LVL Current character level
     * @param aName Character name
     */

    public AbstractPlayers(int ATK, int DEF, int MaxHp, int maximumFp, int LVL,String aName ){
        super(ATK,DEF,MaxHp,LVL,aName);
        fp=maximumFp;
        maxFp=maximumFp;
        vault= new Arsenal();
    }

    /***
     * @return current Fp
     */
    public int getFp() {return fp;}

    /**
     * @return maximum Fp
     */
    public int getMaxFp() {return maxFp;}

    /**
     * @param newFp sets new fp value, but it is always between 0 and maxFp
     */
    public void setFp(int newFp) {fp=limitNumber(0,maxFp,newFp);}

    /**
     * @param amount adds this amount to fp
     */
    public void addFp(int amount){setFp(fp+amount);}

    /***
     * @param item the item we want to check if it is in the arsenal
     * @return true if the player has it or false if it does not
     */
    public boolean isInArsenal(String item) {return vault.isInList(item);}

    /***
     * @param item the item we want to check the amount of
     * @return current item amount the player has
     */
    public int itemAmount(String item) {return vault.getAmount(item);}

    /***
     * @param item the item we want to add amount to
     * @param amount the amount we want to add
     * adds the amount to the item in the players arsenal
     */
    public void addItem(String item, int amount) {vault.addAmount(item,amount);}

    /***
     * @param item the item we want to check
     * @return true if the player has more than 0 of the item or false if not
     */
    public boolean hasItem(String item) {return itemAmount(item)>0;}



    /***
     *  @param item the name of the item we want to use
     *  if the item is in the arsenal and the player has more than 0 of it, it uses the effect on the player and subtracts 1 from the item amount.
     */
    public void useItem(String item) {
        if(isInArsenal(item) && hasItem(item)){
            vault.use(item,this);}}


    /***
     * @param attacker the attacking character
     * This function models the standard interaction of a enemy attacking the player
     */
    protected void getStandardAttacked(Enemies attacker) {minusHp(calculateDmg(0.75,attacker.getAtk(),def,attacker.getLvl()));}

    /***
     * A simple method to print out all the relevant stats
     * @return The string with the stats
     */
    @Override
    public String toString() {
        return  name+":" +
                "  Hp=" + hp + "/" + maxHp+
                ", Atk=" + atk +
                ", Def=" + def +
                ", Lvl=" + lvl +
                ", Fp=" + fp+"/" + maxFp;
    }

    /***
     * This setter is mainly for when various characters share an arsenal ant it overwrites the default one of the player.
     * @param arsenal the bault we are setting for the player
     */
    public void setItems(Arsenal arsenal) {this.vault = arsenal;}

    /***
     * Method for leveling up a player, it adds 15% to both atk and MaxHp; and 1 to
     * the current level.The +1 gives a minimum increase for maxHp and atk and rounds up
     * value.
     */
    public void lvlUp(){
        maxHp= (int) (maxHp*1.15)+1;
        atk = (int) (atk*1.15)+1;
        hp= (int) (hp*1.15)+1;
        def = (int) (def*1.15)+1;
        maxFp= (int) (maxFp*1.15)+1;
        fp = (int) (fp*1.15)+1;
        lvl = lvl + 1;
    }

    /***
     * Equal method for players
     * @param o te character we are comparing to
     * @return True if the attributes are equal, false otherwise
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        if (!super.equals(o)) return false;
        AbstractPlayers that = (AbstractPlayers) o;
        return fp == that.fp && maxFp == that.maxFp;
    }
}

