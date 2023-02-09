package com.example.aventurasdemarcoyluis.model.characters.interfaces;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
/***
 * interface for all enemies that can be effectively jumped attacked by Luis
 */
public interface JumpedAttackedByLuis {
    void getsJumpAttackedByLuis(Luis attacker);
    void attacks(Players player);}
