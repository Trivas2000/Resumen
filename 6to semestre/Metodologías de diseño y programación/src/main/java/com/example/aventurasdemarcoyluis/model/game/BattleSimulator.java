package com.example.aventurasdemarcoyluis.model.game;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.*;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Character;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;
import com.example.aventurasdemarcoyluis.model.game.patterns.phases.NewTurnPhase;
import com.example.aventurasdemarcoyluis.model.game.patterns.phases.StandardPhase;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.*;
import com.example.aventurasdemarcoyluis.model.items.Arsenal;
import com.example.aventurasdemarcoyluis.model.items.interfaces.useItem;

import java.util.ArrayList;

/***
 * The controller class for the game, it is in charge of dealing with the character directly so the view does not have to.
 */
public class BattleSimulator {

    private Marco marco;
    private Luis luis;

    private ArrayList<Players> players;
    private ArrayList<Enemies> enemies;
    private ArrayList<HammerAttackedByLuis> hammerAttackedByLuis = new ArrayList<>();
    private ArrayList<HammerAttackedByMarco> hammerAttackedByMarco = new ArrayList<>();
    private ArrayList<JumpedAttackedByLuis> jumpedAttackedByLuis = new ArrayList<>();
    private ArrayList<Character> aliveCharacters;
    private ArrayList<Boo> boos = new ArrayList<>();

    private Arsenal sharedArsenal;

    private final HammerAttackableVisitor hammerAttackableVisitor = new HammerAttackableVisitor();
    private final AttackableByLuisVisitor attackableByLuisVisitor = new AttackableByLuisVisitor();
    private final CheckIfPlayerVisitor checkIfPlayerVisitor = new CheckIfPlayerVisitor();
    private final CheckIfLuisVisitor checkIfLuisVisitor = new CheckIfLuisVisitor();
    private final CheckIfBooVisitor checkIfBooVisitor = new CheckIfBooVisitor();

    private int turnOwnerIndex;
    private int gameStatus;
    private StandardPhase phase;

    /***
     * The constructor also generates aliveCharacters that is the fusion of players and enemies and starts the
     * turnOwnerIndex and gameStatus at 0
     * @param level The level we are setting the players to
     * @param enemiesIndex An array of enemies indexes to create those enemies in the simulator.
     */
    public BattleSimulator(int level, ArrayList<Integer> enemiesIndex) {
        players = new ArrayList<>();
        marco = new Marco(20, 10, 20, 20, level);
        luis = new Luis(10, 20, 20, 20, level);
        players.add(marco);
        players.add(luis);
        sharedArsenal = new Arsenal();
        playersGetter(0).setItems(sharedArsenal);
        playersGetter(1).setItems(sharedArsenal);

        enemies = new ArrayList<>();
        enemiesAdder(enemiesIndex);


        arrayFusions(players, enemies);

        turnOwnerIndex = 0;
        gameStatus = 0;

    }

    /***
     * Method for starting the controller phase
     */
    public void startGame() throws InvalidPhaseTransitionException {
        phase = new NewTurnPhase();
        phase.setController(this);
        if(checkIfCurrentTurnOwnerIsPlayer()){
            phase.transitionToPlayerStartOfTurnPhase();
        }
        else{
            phase.transitionEnemyToChooseTargetPhase();
        }
    }

    /***
     * The enemiesAdder for the constructor, it adds a Lvl 1 Goomba, Spiny or Boo with their respective
     * base stats to the enemies for each Index in enemies Index associated with the enemy.0 represents a
     * Goomba, 1 a Spiny and 2 a Boo.
     * @param enemiesIndex The list of all te indexes of the enemies we want to add
     */
    public void enemiesAdder(ArrayList<Integer> enemiesIndex) {
        int counter = 0;
        while (enemiesIndex.size() > counter) {
            if (enemiesIndex.get(counter) == 1) {
                Goomba goomba = new Goomba(40, 10, 10, 1);
                enemies.add(goomba);
                hammerAttackedByLuis.add(goomba);
                jumpedAttackedByLuis.add(goomba);
                hammerAttackedByMarco.add(goomba);

            }
            if (enemiesIndex.get(counter) == 2) {
                Spiny spiny = new Spiny(30, 15, 10, 1);
                enemies.add(spiny);
                hammerAttackedByMarco.add(spiny);
                hammerAttackedByLuis.add(spiny);
                jumpedAttackedByLuis.add(spiny);
            }
            if (enemiesIndex.get(counter) == 3) {
                Boo boo = new Boo(50, 5, 10, 1);
                enemies.add(boo);
                hammerAttackedByMarco.add(boo);
                boos.add(boo);
            }
            counter += 1;
        }
    }

    /***
     * Fusions the 2 given arrays into aliveCharacters
     * @param players the players we want to add
     * @param enemies the enemies we want to add
     */
    public void arrayFusions(ArrayList<Players> players, ArrayList<Enemies> enemies) {
        aliveCharacters = new ArrayList<>();
        int c = 0;
        while (players.size() > c) {
            aliveCharacters.add(players.get(c));
            c += 1;
        }
        int c1 = 0;
        while (enemies.size() > c1) {
            aliveCharacters.add(enemies.get(c1));
            c1 += 1;
        }
    }


    /***
     * Returns the enemy of Index asked if we ask for an index higher than the current amount of enemies
     * it cycles the list again until it finds an enemy.
     * @param enemyIndex the index of the enemy we want
     * @return The enemy
     */
    public Enemies enemiesGetter(int enemyIndex) {
        return enemies.get(enemyIndex % enemies.size());
    }

    /***
     * Returns the player of Index asked if we ask for an index higher than the current amount of enemies
     * it cycles the list again until it finds an enemy.
     * @param playerIndex the index of the enemy we want
     * @return The player
     */
    public Players playersGetter(int playerIndex) {
        return players.get(playerIndex % players.size());
    }


    /***
     * Returns the amount of the requested item
     * @param item the item we want the amount of
     * @return item amount
     */
    public int getAmount(String item) {
        return sharedArsenal.getAmount(item);
    }

    /**
     * Adds amount to  a certain item in the arsenal
     *
     * @param item   the item we want to add amount to
     * @param amount the amount we want to add
     */
    public void addAmount(String item, int amount) {
        sharedArsenal.addAmount(item, amount);
    }

    /***
     * Uses the item on the player
     * @param item the item the player is using
     * @param playerIndex the index of the player that is using the item (0 is Marco and 1 is Luis)
     */
    public void use(String item, int playerIndex) {
        if (playerIndex == 0 && !marco.isKod()) {
            marco.useItem(item);
        } else if (playerIndex == 1 && !luis.isKod()) {
            luis.useItem(item);
        }
    }

    /***
     * Method that returns all the current items in an array list
     * @return the array list with all the items
     */
    public ArrayList<useItem> getItems() {
        return sharedArsenal.getItemList();
    }

    /***
     * Getter for aliveCharacters
     * @return the array of alive characters
     */
    public ArrayList<Character> getAliveCharacters() {
        return aliveCharacters;
    }

    /***
     * Getter for enemies
     * @return the array of enemies
     */
    public ArrayList<Enemies> getEnemies() {
        return enemies;
    }

    /***
     * Getter for players
     * @return the array of players
     */
    public ArrayList<Players> getPlayers() {
        return players;
    }

    /***
     * Method for getting the character that has the turn
     * @return the current character with the turn
     */
    public Character currentTurnCharacter() {
        return aliveCharacters.get(turnOwnerIndex);
    }

    /***
     * Method for getting the character who will have the turn next
     * @return the character who will have the turn next
     */
    public Character nextTurnCharacter() {
        return aliveCharacters.get((turnOwnerIndex + 1) % aliveCharacters.size());
    }

    /***
     * Advances the turn, so it changes the current turn owner by adding 1 to the index.
     * The % makes it cycle.
     */
    public void advanceTurn() {
        turnOwnerIndex = (turnOwnerIndex + 1) % aliveCharacters.size();
    }

    /***
     * Checks what the current status of the game should be and changes it.
     */
    public void statusChecker() {
        if (enemies.size() == 0) {
            gameStatus = 1;
        } else if (players.size() == 1) {
            gameStatus = 2;
        }
    }

    /***
     * Checks for all players to see if they are Kod, if they are they get removed from players and aliveCharacters
     */
    public void playersKoChecker() {
        int c = 0;
        while (players.size() > c && players.size() != 0) {
            if (players.get(c).isKod()) {
                players.remove(c);
                arrayFusions(players, enemies);
                statusChecker();
            }
            c += 1;
        }
    }

    /***
     * Checks for all enemies to see if they are Kod, if they are they get removed from enemies and aliveCharacters
     */
    public void enemiesKoChecker() {
        int c = 0;
        while (enemies.size() > c && enemies.size() != 0) {
            if (enemies.get(c).isKod()) {
                enemies.remove(c);
                arrayFusions(players, enemies);
                statusChecker();
                c -= 1;
            }
            c += 1;

        }
    }

    /***
     * Method for damaging a character, it also updates the lists and gameStatus
     * @param characterIndex the index of the character we want to damage
     * @param amount the amount of hp to subtract
     */
    public void damageCharacter(int characterIndex, int amount) {
        aliveCharacters.get(characterIndex).minusHp(amount);
        enemiesKoChecker();
        playersKoChecker();
    }

    /***
     * Sets Marcos random seed
     * @param seed the seed we are setting
     */
    public void setSeed(int seed) {
        playersGetter(0).setSeed(seed);
    }

    /***
     * Generates a random index array
     * @param min the minimum value for the array
     * @param max the maximum value for the array
     * @param amount the amount of elements in the array
     * @return the random array
     */
    public ArrayList<Integer> randomIndexGenerator(int min, int max, int amount) {
        ArrayList<Integer> indexList = new ArrayList<>();
        int c = 0;
        while (amount > c) {
            indexList.add(playersGetter(0).generateRandomInt(min, max));

            c += 1;
        }
        return indexList;
    }

    /***
     * Getter for game status, value 0 means no one has won; 1 means the players won and 2 means the enemies won
     * @return current gameStatus
     */
    public int getGameStatus() {
        return gameStatus;
    }

    /***
     * Randomizes the enemies of the battleSimulator
     * @param amount the amount of enemies
     */
    public void randomizeEnemies(int amount) {
        enemies = new ArrayList<>();
        enemiesAdder(randomIndexGenerator(1, 3, amount));
    }

    /***
     * Method for a marco attack
     * @param enemyIndex the index of the enemy
     * @param attackIndex the index of the attack
     */
    public void marcoAttack(int enemyIndex, int attackIndex) {
        enemiesGetter(enemyIndex).accept(hammerAttackableVisitor);

        if (attackIndex == 1) {
            marco.jumpAttacks(enemiesGetter(enemyIndex));
        } else if (attackIndex == 2 && hammerAttackableVisitor.getResult()) {
            marco.hammerAttacks(hammerAttackedByMarco.get(hammerAttackedByMarco.indexOf((enemiesGetter(enemyIndex)))));
        }
        enemiesKoChecker();
        playersKoChecker();
    }

    /***
     * Method for a luis attack
     * @param enemyIndex the index of the enemy
     * @param attackIndex the index of the attack
     */
    public void luisAttack(int enemyIndex, int attackIndex) {
        enemiesGetter(enemyIndex).accept(hammerAttackableVisitor);
        enemiesGetter(enemyIndex).accept(attackableByLuisVisitor);

        if (attackIndex == 1 && attackableByLuisVisitor.getResult()) {
            luis.jumpAttacks(jumpedAttackedByLuis.get(jumpedAttackedByLuis.indexOf(enemiesGetter(enemyIndex))));
        } else if (attackIndex == 2 && hammerAttackableVisitor.getResult() && attackableByLuisVisitor.getResult()) {
            luis.hammerAttacks(hammerAttackedByLuis.get(hammerAttackedByLuis.indexOf(enemiesGetter(enemyIndex))));
        }
        enemiesKoChecker();
        playersKoChecker();
    }

    /***
     * Setter for phase it also sets the controller as the controller of the phase
     * @param newPhase the new phase of the simulator
     */
    public void setPhase(StandardPhase newPhase) {
        this.phase = newPhase;
        phase.setController(this);
    }

    /***
     * Checks it he current turn owner is a player
     * @return true if it is false otherwise
     */
    public boolean checkIfCurrentTurnOwnerIsPlayer() {
        currentTurnCharacter().acceptGeneral(checkIfPlayerVisitor);
        return checkIfPlayerVisitor.getResult();
    }

    /***
     * Method for choosing red mushroom
     * @throws InvalidPhaseTransitionException when cannot transition
     * @throws InvalidActionException when you can not perform an action
     */
    public void chooseRedMushroom() throws InvalidPhaseTransitionException, InvalidActionException {
        phase.chooseItem(1);
    }

    /***
     * Method for choosing honey syrup
     * @throws InvalidPhaseTransitionException when cannot transition
     * @throws InvalidActionException when you can not perform an action
     */
    public void chooseHoneySyrup() throws InvalidPhaseTransitionException, InvalidActionException {
        phase.chooseItem(2);
    }

    /***
     * Method for choosing to use an item on marco
     * @throws InvalidPhaseTransitionException when cannot transition
     * @throws InvalidActionException when you can not perform an action
     */
    public void chooseUseItemOnMarco() throws InvalidPhaseTransitionException, InvalidActionException {
        phase.choosePlayer(0);
        phase.useItem();
        phase.endTurn();

    }
    /***
     * Method for choosing to use an item on luis
     * @throws InvalidPhaseTransitionException when cannot transition
     * @throws InvalidActionException when you can not perform an action
     */
    public void chooseUseItemOnLuis() throws InvalidPhaseTransitionException, InvalidActionException {
        phase.choosePlayer(1);
        phase.useItem();
        phase.endTurn();


    }

    /***
     * Method for when the player decides to use an item
     */
    public void chooseToUseItem(){
        try{phase.transitionToChoosingItemPhase();}
        catch (InvalidPhaseTransitionException e){
            e.printStackTrace();
        }
    }

    /***
     * Method for when the player decides to pass its turn
     */
    public void passTurn(){
       try{
           phase.transitionToPassTurnPhase();
           phase.playerPassTurn();
           phase.endTurn();}
       catch (InvalidPhaseTransitionException | InvalidActionException e){
           e.printStackTrace();}
    }

    /***
     * Method for when the player decides to attack
     */
    public void chooseToAttack(){
        try{phase.transitionToChoosingAttackPhase();}
        catch (InvalidPhaseTransitionException e){
            e.printStackTrace();
        }
    }

    /***
     * Method for choosing jump attack
     */
    public void chooseJumpAttack() {
        try {
            phase.chooseAttackType(1);
        } catch (InvalidPhaseTransitionException | InvalidActionException e) {
            e.printStackTrace();}}

    /***
     * Method for choosing hammer attack
     */
    public void chooseHammerAttack() {
        try {
            phase.chooseAttackType(2);
        } catch (InvalidPhaseTransitionException | InvalidActionException e) {
            e.printStackTrace();}}

    /***
     * Method for attacking an enemy
     */
    public void attackEnemy(int enemyIndex)  {
        try{phase.phaseAttack(enemyIndex);
            phase.endTurn();}
        catch (InvalidPhaseTransitionException|InvalidActionException e){
            e.printStackTrace();
        }
    }

    /***
     * Getter for phase
     * @return current phase
     */
    public StandardPhase getPhase() {
        return phase;
    }

    /***
     * Checks if the current character is a luis
     * @return true if it is, false otherwise
     */
    public boolean checkIfCurrentTurnIsLuis(){
        currentTurnCharacter().acceptGeneral(checkIfLuisVisitor);
        return checkIfLuisVisitor.getResult();
    }

    /***
     * Checks if the current character is a boo
     * @return true if it is, false otherwise
     */
    public boolean checkIfCurrentTurnIsBoo(){
        currentTurnCharacter().acceptGeneral(checkIfBooVisitor);
        return checkIfBooVisitor.getResult();
    }

    /***
     * Checks if luis is kod
     * @return true if he is false otherwise
     */
    public boolean isLuisKod(){
        return luis.isKod();
    }


    /***
     * Checks if marco is kod
     * @return true if he is false otherwise
     */
    public boolean isMarcoKod(){
        return marco.isKod();
    }

    /***
     * Method for enemy attack
     * @param playerIndex the index of the player we want to attack
     */
    public void enemyAttack(int playerIndex) {

        if (!checkIfCurrentTurnIsBoo() && playerIndex==1) {
            jumpedAttackedByLuis.get(jumpedAttackedByLuis.indexOf(currentTurnCharacter())).attacks(marco);
        }
        else if(!checkIfCurrentTurnIsBoo() && playerIndex==2) {
            jumpedAttackedByLuis.get(jumpedAttackedByLuis.indexOf(currentTurnCharacter())).attacks(luis);

        }
        else if (checkIfCurrentTurnIsBoo()){
            boos.get(boos.indexOf(currentTurnCharacter())).attacks(luis);
        }
        enemiesKoChecker();
        playersKoChecker();
    }
}



