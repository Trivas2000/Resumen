package com.example.aventurasdemarcoyluis.model.characters.interfaces;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;

/**This interface is here so that we do not have to instance Luis when Boo is attacking someone, and if in 
 * the future we want other kind of players to be attacked by boo we just implement this interface
 */
public interface AttackedByBoo {
    void getsAttackedByBoo(Boo boo);
}
