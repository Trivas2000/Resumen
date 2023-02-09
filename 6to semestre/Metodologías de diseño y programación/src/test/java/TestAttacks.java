import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestAttacks {

    private Goomba testGoomba;
    private Marco testMarco;
    private Luis testLuis;
    private Spiny testSpiny;
    private Boo testBoo;

    @BeforeEach
    public void setUp() {
        testGoomba = new Goomba(80, 10, 100, 8);
        testMarco = new Marco(100, 20, 200, 12, 1);
        testLuis = new Luis(100, 15, 100, 12, 1);
        testSpiny = new Spiny(80, 10, 100, 4);
        testBoo = new Boo(40, 5, 200, 1);

    }

    @Test
    public void attackTestPlayerJumpAttack() {
        assertEquals(100, testGoomba.getHp());/**Marco vs Goomba*/
        testMarco.jumpAttacks(testGoomba);
        assertEquals(90, testGoomba.getHp());
        testMarco.setHp(0);
        testMarco.jumpAttacks(testGoomba);
        assertEquals(90, testGoomba.getHp());

        testGoomba.setHp(100);
        assertEquals(100, testGoomba.getHp());/**Luis vs Goomba*/
        testLuis.jumpAttacks(testGoomba);
        assertEquals(90, testGoomba.getHp());
        testLuis.setHp(0);
        testLuis.jumpAttacks(testGoomba);
        assertEquals(90, testGoomba.getHp());

        testMarco.setHp(10);
        assertEquals(200, testBoo.getHp());/**Marco vs boo*/
        testMarco.jumpAttacks(testBoo);
        assertEquals(180, testBoo.getHp());
        testMarco.setHp(0);
        testMarco.jumpAttacks(testBoo);
        assertEquals(180, testBoo.getHp());
    }

    @Test
    public void attackTestGoomba() {
        assertEquals(200, testMarco.getHp());/**Goomba vs marco*/
        testGoomba.attacks(testMarco);
        assertEquals(176, testMarco.getHp());
        testGoomba.setHp(0);
        testGoomba.attacks(testMarco);
        assertEquals(176, testMarco.getHp());

        testGoomba.setHp(20);
        assertEquals(100, testLuis.getHp());/**Goomba vs Luis*/
        testGoomba.attacks(testLuis);
        assertEquals(68, testLuis.getHp());
        testGoomba.setHp(0);
        testGoomba.attacks(testLuis);
        assertEquals(68, testLuis.getHp());}


    @Test
    public void attackTestBoo() {
        assertEquals(100, testLuis.getHp());/**Boo vs Luis*/
        testBoo.attacks(testLuis);
        assertEquals(98, testLuis.getHp());
        testBoo.setHp(0);
        testBoo.attacks(testLuis);
        assertEquals(98, testLuis.getHp());}

    @Test
    public void attackTestSpiny() {
        assertEquals(200, testMarco.getHp());/**Spiny vs marco*/
        testSpiny.attacks(testMarco);
        assertEquals(188, testMarco.getHp());
        testSpiny.setHp(0);
        testSpiny.attacks(testMarco);
        assertEquals(188, testMarco.getHp());

        testSpiny.setHp(20);
        assertEquals(100, testLuis.getHp());/**Spiny vs Luis*/
        testSpiny.attacks(testLuis);
        assertEquals(84, testLuis.getHp());
        testSpiny.setHp(0);
        testSpiny.attacks(testLuis);
        assertEquals(84, testLuis.getHp());}

    @Test
    public void attackTestSpinyDmg() {
        assertEquals(100, testSpiny.getHp()); /**Luis jumps spiny*/
        testLuis.jumpAttacks(testSpiny);
        assertEquals(95, testLuis.getHp());
        assertEquals(100, testSpiny.getHp());
        testLuis.setHp(4);
        testLuis.jumpAttacks(testSpiny);
        assertEquals(0, testLuis.getHp());
        assertEquals(100, testSpiny.getHp());

        assertEquals(100, testSpiny.getHp()); /**Marco jumps spiny*/
        testMarco.jumpAttacks(testSpiny);
        assertEquals(190, testMarco.getHp());
        assertEquals(100, testSpiny.getHp());
        testMarco.setHp(8);
        testMarco.jumpAttacks(testSpiny);
        assertEquals(0, testMarco.getHp());
        assertEquals(100, testSpiny.getHp());
    }


    @Test
    public void hammerAttackLuis() {
        testSpiny.setSeed(2); /** Seed 2 makes it so the hammer attack is successful*/
        assertEquals(100, testSpiny.getHp());
        testLuis.hammerAttacks(testSpiny);
        assertEquals(100, testLuis.getHp());
        assertEquals(85, testSpiny.getHp());
        testSpiny.setHp(10);
        testLuis.hammerAttacks(testSpiny);
        assertEquals(0, testSpiny.getHp());
        assertEquals(100, testLuis.getHp());

        testSpiny.setSeed(1);/** Seed 1 makes it so the hammer attack is unsuccessful*/
        testSpiny.setHp(50);
        assertEquals(50, testSpiny.getHp());
        testLuis.hammerAttacks(testSpiny);}



    @Test
    public void fpUsesWhenAttacking() {
        assertEquals(12, testMarco.getFp());
        testMarco.jumpAttacks(testGoomba);
        assertEquals(11, testMarco.getFp());
        testMarco.hammerAttacks(testSpiny);
        assertEquals(9, testMarco.getFp());

        testMarco.setHp(0);
        testMarco.jumpAttacks(testGoomba);
        assertEquals(9, testMarco.getFp());
        testMarco.hammerAttacks(testSpiny);
        assertEquals(9, testMarco.getFp());}


}
