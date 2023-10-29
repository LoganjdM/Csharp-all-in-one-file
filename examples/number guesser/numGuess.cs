using System;

namespace NumberGuessGame
{
    class Program
    {
        static void Main()
        {
            Console.WriteLine("Welcome to number guesser!");
            while(true)
            {
                sissyphusRollingBoulderUpHill();
            }
        }
        static void sissyphusRollingBoulderUpHill()
        {
            Console.WriteLine("I'm thinking of a number between 1 and 100...");

            Guess guesser = new Guess(new Random().Next(1, 101));
            while (!guesser.guessing())
            {
                Console.WriteLine("Try again...");
            }

            Console.WriteLine("Thanks for playing!\n"); //  2 line spacing before restart looks nice  //
        }
    }
    public class Guess
    {
        int secretNumber {get;} //  does not change  //
        uint attempts {get; set;}
        public Guess(int num)
        {
            this.secretNumber = num;
            this.attempts = 1;
        }
        public bool guessing()
        {
            Console.Write("Enter your guess: ");
            if (!int.TryParse(Console.ReadLine(), out int userGuess))
            {
                Console.WriteLine("Invalid input. Please enter a valid number.");
                return false;
            }

            if (userGuess == secretNumber)
            {
                Console.WriteLine($"Congratulations! You guessed the number {this.secretNumber} in {this.attempts} attempts.");
                return true;
            }
            this.attempts++;

            higherOrLower(secretNumber,userGuess);
            return false;
        }
        static void higherOrLower(int secretNumber, int guess)
        {
            if (guess < secretNumber)
                Console.WriteLine("Higher number.");
            else
                Console.WriteLine("Lower number.");
        }
    }
}