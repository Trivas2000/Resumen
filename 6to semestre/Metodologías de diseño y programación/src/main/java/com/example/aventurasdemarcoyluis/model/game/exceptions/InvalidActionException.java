package com.example.aventurasdemarcoyluis.model.game.exceptions;

/***
 * Exception for invalid actions
 */
public class InvalidActionException extends Exception{
    public InvalidActionException(final String message){
        super(message);
    }
}