using System;

namespace NumGuess2
{
    public struct Guess
    {
        int secretNumber { get; } //  does not change  //
        uint attempts { get; set; }
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

            higherOrLower(secretNumber, userGuess);
            return false;
        }
        static void higherOrLower(int secretNumber, int guess)
        {
            if (userGuess < secretNumber)
                Console.WriteLine("Higher number.");
            else
                Console.WriteLine("Lower number.");
        }
    }
}