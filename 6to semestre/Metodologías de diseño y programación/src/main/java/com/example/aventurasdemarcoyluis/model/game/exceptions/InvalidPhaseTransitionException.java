package com.example.aventurasdemarcoyluis.model.game.exceptions;

/***
 * Exception for invalid phase transitions
 */
public class InvalidPhaseTransitionException extends Exception{
    public InvalidPhaseTransitionException(final String message){
        super(message);
    }
}