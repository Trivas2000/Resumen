
import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.game.BattleSimulator;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.items.Arsenal;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

public class TestBattleSimulation {

    private BattleSimulator testBattleSimulator;
    private Marco testMarco;
    private Luis testLuis;
    private Spiny testSpiny;
    private Boo testBoo;
    private Goomba testGoomba;

    @BeforeEach
    public void setUp() {

        testSpiny = new Spiny(30, 15, 10, 1);
        testBoo = new Boo(50, 5, 10, 1);
        testGoomba = new Goomba(40, 10, 10, 1);
        testMarco=new Marco(20,10,20,20,1);
        testLuis=new Luis(10,20,20,20,1);

        ArrayList<Integer> enemiesIndex;
        enemiesIndex = new ArrayList();
        enemiesIndex.add(1);
        enemiesIndex.add(2);
        enemiesIndex.add(3);
        testBattleSimulator = new BattleSimulator(1,enemiesIndex);
    }

    @Test
    public void ConstructingPlayersTest() {
        assertEquals(testBattleSimulator.playersGetter(1).getHp(), testLuis.getHp());
        assertEquals(testBattleSimulator.playersGetter(1).getAtk(), testLuis.getAtk());
        assertEquals(testBattleSimulator.playersGetter(1).getLvl(), testLuis.getLvl());
        assertEquals(testBattleSimulator.playersGetter(1).getDef(), testLuis.getDef());
        assertEquals(testBattleSimulator.playersGetter(1).getFp(), testLuis.getFp());
        assertEquals(testBattleSimulator.playersGetter(1).getHp(), testLuis.getHp());

        assertEquals(testBattleSimulator.playersGetter(0).getHp(), testMarco.getHp());
        assertEquals(testBattleSimulator.playersGetter(0).getAtk(), testMarco.getAtk());
        assertEquals(testBattleSimulator.playersGetter(0).getDef(), testMarco.getDef());
        assertEquals(testBattleSimulator.playersGetter(0).getFp(), testMarco.getFp());
        assertEquals(testBattleSimulator.playersGetter(0).getHp(), testMarco.getHp());
    }
    @Test
    public void ConstructingEnemiesTest() {
        assertEquals(testBattleSimulator.enemiesGetter(0).getHp(),testGoomba.getHp());
        assertEquals(testBattleSimulator.enemiesGetter(0).getAtk(),testGoomba.getAtk());
        assertEquals(testBattleSimulator.enemiesGetter(3).getDef(),testGoomba.getDef());
        assertEquals(testBattleSimulator.enemiesGetter(6).getLvl(),testGoomba.getLvl());

        assertEquals(testBattleSimulator.enemiesGetter(1).getHp(),testSpiny.getHp());
        assertEquals(testBattleSimulator.enemiesGetter(1).getAtk(),testSpiny.getAtk());
        assertEquals(testBattleSimulator.enemiesGetter(4).getDef(),testSpiny.getDef());
        assertEquals(testBattleSimulator.enemiesGetter(7).getLvl(),testSpiny.getLvl());

        assertEquals(testBattleSimulator.enemiesGetter(2).getHp(),testBoo.getHp());
        assertEquals(testBattleSimulator.enemiesGetter(2).getAtk(),testBoo.getAtk());
        assertEquals(testBattleSimulator.enemiesGetter(5).getDef(),testBoo.getDef());
        assertEquals(testBattleSimulator.enemiesGetter(8).getLvl(),testBoo.getLvl());
    }

    @Test
    public void ConstructingRandomEnemiesTest() {
        testBattleSimulator.setSeed(2);
        testBattleSimulator.randomizeEnemies(3);
        assertEquals(testSpiny,testBattleSimulator.enemiesGetter(0));
        assertEquals(testGoomba,testBattleSimulator.enemiesGetter(1));
        assertEquals(testBoo,testBattleSimulator.enemiesGetter(2));

    }

    @Test
    public void arsenalCreatorTest(){
        assertEquals(0,testBattleSimulator.getAmount("Red Mushroom"));
        assertEquals(testBattleSimulator.getAmount("Red Mushroom"),testBattleSimulator.playersGetter(1).itemAmount("Red Mushroom"));
        assertEquals(testBattleSimulator.playersGetter(1).itemAmount("Red Mushroom"),testBattleSimulator.playersGetter(0).itemAmount("Red Mushroom"));

        testBattleSimulator.addAmount("Red Mushroom",3);

        assertEquals(3,testBattleSimulator.getAmount("Red Mushroom"));
        assertEquals(testBattleSimulator.getAmount("Red Mushroom"),testBattleSimulator.playersGetter(1).itemAmount("Red Mushroom"));
        assertEquals(testBattleSimulator.playersGetter(1).itemAmount("Red Mushroom"),testBattleSimulator.playersGetter(0).itemAmount("Red Mushroom"));

        testBattleSimulator.addAmount("Honey Syrup",10);

        assertEquals(10,testBattleSimulator.getAmount("Honey Syrup"));
        assertEquals(testBattleSimulator.getAmount("Honey Syrup"),testBattleSimulator.playersGetter(1).itemAmount("Honey Syrup"));
        assertEquals(testBattleSimulator.playersGetter(1).itemAmount("Honey Syrup"),testBattleSimulator.playersGetter(0).itemAmount("Honey Syrup"));
    }

    @Test
    public void itemUseTest(){
        testBattleSimulator.addAmount("Red Mushroom",3);
        assertEquals(3,testBattleSimulator.getAmount("Red Mushroom"));
        testBattleSimulator.playersGetter(1).setHp(1);

        testBattleSimulator.use("Red Mushroom",1);

        assertEquals(3,testBattleSimulator.playersGetter(1).getHp());
        assertEquals(2,testBattleSimulator.getAmount("Red Mushroom"));
    }

    @Test
    public void arsenalReturnTest(){
        testBattleSimulator.addAmount("Red Mushroom",3);
        testBattleSimulator.addAmount("Honey Syrup",1);

        Arsenal testArsenal = new Arsenal();
        testArsenal.addAmount("Red Mushroom",3);
        testArsenal.addAmount("Honey Syrup",1);

        assertEquals(testBattleSimulator.getItems(),testArsenal.getItemList());
    }

    @Test
    public void aliveCharacterGetterTest(){
        testBattleSimulator.arrayFusions(testBattleSimulator.getPlayers(),testBattleSimulator.getEnemies());
        assertEquals(testMarco,testBattleSimulator.getAliveCharacters().get(0));
        assertEquals(testLuis,testBattleSimulator.getAliveCharacters().get(1));
        assertEquals(testGoomba,testBattleSimulator.getAliveCharacters().get(2));
        assertEquals(testSpiny,testBattleSimulator.getAliveCharacters().get(3));
        assertEquals(testBoo,testBattleSimulator.getAliveCharacters().get(4));

    }

    @Test
    public void turnGetterTest(){
        assertEquals(testMarco,testBattleSimulator.currentTurnCharacter());
        assertEquals(testLuis,testBattleSimulator.nextTurnCharacter());
        testBattleSimulator.advanceTurn();

        assertEquals(testLuis,testBattleSimulator.currentTurnCharacter());
        assertEquals(testGoomba,testBattleSimulator.nextTurnCharacter());
        testBattleSimulator.advanceTurn();

        assertEquals(testGoomba,testBattleSimulator.currentTurnCharacter());
        assertEquals(testSpiny,testBattleSimulator.nextTurnCharacter());
        testBattleSimulator.advanceTurn();
        testBattleSimulator.advanceTurn();

        assertEquals(testBoo,testBattleSimulator.currentTurnCharacter());
        assertEquals(testMarco,testBattleSimulator.nextTurnCharacter());
        testBattleSimulator.advanceTurn();

        assertEquals(testMarco,testBattleSimulator.currentTurnCharacter());
        assertEquals(testLuis,testBattleSimulator.nextTurnCharacter());
    }

    @Test
    public void removeKodTest() {
        testBattleSimulator.getEnemies().get(0).setHp(0);
        testBattleSimulator.enemiesKoChecker();
        assertEquals(testSpiny,testBattleSimulator.getEnemies().get(0));
        assertEquals(testSpiny,testBattleSimulator.getAliveCharacters().get(2));

        testBattleSimulator.playersGetter(0).setHp(0);
        testBattleSimulator.playersKoChecker();
        assertEquals(testLuis,testBattleSimulator.getPlayers().get(0));
        assertEquals(testLuis,testBattleSimulator.getAliveCharacters().get(0));
        assertEquals(testSpiny,testBattleSimulator.getAliveCharacters().get(1));
    }

    @Test
    public void gameStatusTest1() {
        testBattleSimulator.getEnemies().get(0).setHp(0);
        testBattleSimulator.getEnemies().get(1).setHp(0);
        testBattleSimulator.getEnemies().get(2).setHp(0);
        testBattleSimulator.enemiesKoChecker();
        assertEquals(1,testBattleSimulator.getGameStatus());
    }

    @Test
    public void gameStatusTest2() {
        testBattleSimulator.playersGetter(1).setHp(0);
        testBattleSimulator.playersGetter(1).setHp(0);
        testBattleSimulator.playersKoChecker();
        assertEquals(2,testBattleSimulator.getGameStatus());
    }

    @RepeatedTest(100)
    public void battleSimulatorAttackTest() {

        testBattleSimulator.enemiesGetter(0).setSeed(1);

        assertEquals(10,testBattleSimulator.enemiesGetter(0).getHp());
        testBattleSimulator.marcoAttack(0,1);
        assertEquals(8,testBattleSimulator.enemiesGetter(0).getHp());
        testBattleSimulator.marcoAttack(0,2);


        assertEquals(5,testBattleSimulator.enemiesGetter(0).getHp());


        assertEquals(10,testBattleSimulator.enemiesGetter(2).getHp());
        testBattleSimulator.marcoAttack(2,1);
        assertEquals(6,testBattleSimulator.enemiesGetter(2).getHp());
        testBattleSimulator.marcoAttack(2,2);
        assertEquals(6,testBattleSimulator.enemiesGetter(2).getHp());

        testBattleSimulator.luisAttack(2,1);
        assertEquals(6,testBattleSimulator.enemiesGetter(2).getHp());
        testBattleSimulator.luisAttack(2,2);
        assertEquals(6,testBattleSimulator.enemiesGetter(2).getHp());

        assertEquals(20,testBattleSimulator.playersGetter(1).getHp());
        assertEquals(10,testBattleSimulator.enemiesGetter(1).getHp());
        testBattleSimulator.luisAttack(1,1);
        assertEquals(19,testBattleSimulator.playersGetter(1).getHp());
        assertEquals(10,testBattleSimulator.enemiesGetter(1).getHp());
    }

    @Test
    public void battleSimulation(){
    assertEquals(20,testBattleSimulator.playersGetter(0).getHp());
    assertEquals(20,testBattleSimulator.playersGetter(1).getHp());
    assertEquals(10,testBattleSimulator.enemiesGetter(0).getHp());
    assertEquals(10,testBattleSimulator.enemiesGetter(1).getHp());
    assertEquals(10,testBattleSimulator.enemiesGetter(2).getHp());
    assertEquals(0,testBattleSimulator.getGameStatus());

    testBattleSimulator.addAmount("Red Mushroom",3);
    testBattleSimulator.addAmount("Honey Syrup",3);
    testBattleSimulator.damageCharacter(3,5);
    testBattleSimulator.damageCharacter(4,5);
    testBattleSimulator.damageCharacter(1,3);
    testBattleSimulator.damageCharacter(0,6);
    assertEquals(14,testBattleSimulator.playersGetter(0).getHp());
    assertEquals(17,testBattleSimulator.playersGetter(1).getHp());
    assertEquals(10,testBattleSimulator.enemiesGetter(0).getHp());
    assertEquals(5,testBattleSimulator.enemiesGetter(1).getHp());
    assertEquals(5,testBattleSimulator.enemiesGetter(2).getHp());
    assertEquals(0,testBattleSimulator.getGameStatus());

    testBattleSimulator.use("Red Mushroom",0);
    testBattleSimulator.damageCharacter(3,5);
    testBattleSimulator.damageCharacter(1,4);
    assertEquals(16,testBattleSimulator.playersGetter(0).getHp());
    assertEquals(13,testBattleSimulator.playersGetter(1).getHp());
    assertEquals(10,testBattleSimulator.enemiesGetter(0).getHp());
    assertEquals(5,testBattleSimulator.enemiesGetter(1).getHp());
    assertEquals(0,testBattleSimulator.getGameStatus());

    testBattleSimulator.damageCharacter(2,5);
    testBattleSimulator.damageCharacter(3,5);
    testBattleSimulator.damageCharacter(0,6);
    assertEquals(10,testBattleSimulator.playersGetter(0).getHp());
    assertEquals(13,testBattleSimulator.playersGetter(1).getHp());
    assertEquals(5,testBattleSimulator.enemiesGetter(0).getHp());
    assertEquals(0,testBattleSimulator.getGameStatus());

    testBattleSimulator.damageCharacter(2,5);
    assertEquals(10,testBattleSimulator.playersGetter(0).getHp());
    assertEquals(13,testBattleSimulator.playersGetter(1).getHp());
    assertEquals(1,testBattleSimulator.getGameStatus());
    }



}
