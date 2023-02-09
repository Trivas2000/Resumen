package com.example.aventurasdemarcoyluis.model.characters.AbstractClasses;

import com.example.aventurasdemarcoyluis.model.characters.interfaces.Character;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.CharacterVisitor;

import java.util.Objects;
import java.util.Random;

/**
 * AbstractCharacter is going to be the base for all the different character classes.
 * It contains the common methods and attributes that al characters will share.
 * It implements character so that we can call that interface for methods associated with general characters like calculate damage
 * */

public abstract class AbstractCharacter implements Character {

    protected int atk;
    protected int def;
    protected int maxHp;
    protected int hp;
    protected int lvl;
    protected final String name;

    /**
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param MaxHp amount of hit points
     * @param LVL Current character level
     * @param Name Character name
     */

    public AbstractCharacter(int ATK, int DEF, int MaxHp, int LVL,String Name) {
        atk = ATK;
        def = DEF;
        maxHp = MaxHp;
        hp = MaxHp;
        lvl = LVL;
        name=Name;}


    /***
     * @return attack points
     */
    public int getAtk() {return this.atk;}

    /**
     * @return defense points
     */
    public int getDef() {return def;}

    /**
     * @return current Hp
     */
    public int getHp() {return hp;}

    /***
     * @return maximum Hp
     */
    public int getMaxHp() {return maxHp;}

    /**
     * @return current Level
     */
    public int getLvl() {return lvl;}

    /***
     * @return the character name
     */
    public String getType(){return name;}

    /***
     * @param atk changes attack points to the given int
     */
    public void setAtk(int atk) {this.atk = atk;}

    /***
     * @param def changes defense points to the given int
     */
    public void setDef(int def) {this.def = def;}

    /***
     * @param hp sets new hp value, but it is always between 0 and maxHp
     */
    public void setHp(int hp){this.hp=limitNumber(0,this.maxHp,hp);}

    /***
     * @param amount subtracts the amount given from current hp
     */
    public void minusHp(int amount){setHp(hp-amount);}

    /***
     * @param minimum the lower limit for number
     * @param maximum the upper limit for number
     * @param number the number we want to limit
     * @return  the limited number between minimum and maximum
     */
    protected int limitNumber(int minimum,int maximum,int number) {

        assert (minimum <= maximum);

        if (number < minimum) {return minimum;}

        if (number > maximum) {return maximum;}

        else {return number;}}

    /***
     * @return true if the character is alive(hp>0) or false if it is ko'd (hp=0)
     */
    public boolean isKod() {return this.getHp() == 0;}

    /***
     * @param k the k multiplier for the attack
     * @param attackerAttack the attacker attack
     * @param attackerLvl the attacker level
     * @param defenderDefense the defender defense
     * @return the amount of damage the attacker should deal to the defender
     */
    protected int calculateDmg(double k,int attackerAttack,int defenderDefense,int attackerLvl){
        return (int) (k*attackerAttack*attackerLvl/defenderDefense);}


    /***we generate this random so that we can seed it to get an exact value while testing*/
    private Random random = new Random();
    /***
     * Generates a random int between min and max, source(https://www.baeldung.com/java-generating-random-numbers-in-range)
     * @param min minimum possible int
     * @param max maximum possible int
     * @return random int between min and max
     */
    public int generateRandomInt(int min, int max) {
        return random.nextInt(max+1 - min) + min;}

    /**
     * Sets the seed for random
     * @param seed the seed we set
     */
    public void setSeed(final long seed) {random.setSeed(seed);}

    /***
     * Used to get 1 75% of the time and 0 the other 25%
     * @return 1 or O
     */
    protected int seventyFivePercent(){
        int randomNumber = generateRandomInt(1, 4);
        if (randomNumber>1) return 1;
        else return 0;
    }

    /***
     * New equal method based on the attributes of a character
     * @param o te character we are comparing to
     * @return true if they are the same, false otherwise
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AbstractCharacter that = (AbstractCharacter) o;
        return atk == that.atk && def == that.def && maxHp == that.maxHp && hp == that.hp && lvl == that.lvl && Objects.equals(name, that.name) ;
    }

    public abstract void acceptGeneral(CharacterVisitor visitor);

}