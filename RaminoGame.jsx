import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Clock, Plus, Minus } from 'lucide-react';

const RaminoGame = () => {
  const [gameStarted, setGameStarted] = useState(false);
  const [playerCount, setPlayerCount] = useState(3);
  const [players, setPlayers] = useState(Array(3).fill(''));
  const [firstDealer, setFirstDealer] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [handStartTime, setHandStartTime] = useState(null);
  
  const initialGames = [
    { id: 1, name: 'Coppia', description: 'Coppia figurata (J, Q, K, A)', completed: false, scores: {}, time: 0 },
    { id: 2, name: 'Doppia Coppia', description: 'Doppia coppia, una figurata', completed: false, scores: {}, time: 0 },
    { id: 3, name: 'Tris', description: 'Qualsiasi tris', completed: false, scores: {}, time: 0 },
    { id: 4, name: 'Full', description: 'Qualsiasi full', completed: false, scores: {}, time: 0 },
    { id: 5, name: 'Scala 40', description: 'Scala da 40 punti esatti', completed: false, scores: {}, time: 0 },
    { id: 6, name: 'Poker', description: 'Qualsiasi poker', completed: false, scores: {}, time: 0 },
    { id: 7, name: 'Scala Colore', description: 'Scala di 5 carte dello stesso seme', completed: false, scores: {}, time: 0 },
    { id: 8, name: 'Chiusura in Mano', description: 'Apertura = chiusura senza scarto', completed: false, scores: {}, time: 0 }
  ];

  const [games, setGames] = useState([]);
  const [currentGame, setCurrentGame] = useState(0);
  const [scores, setScores] = useState({});

  useEffect(() => {
    let timer;
    if (gameStarted && !allGamesCompleted && handStartTime) {
      timer = setInterval(() => {
        setElapsedTime(Math.floor((Date.now() - handStartTime) / 1000));
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [gameStarted, handStartTime]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const adjustPlayerCount = (increment) => {
    const newCount = playerCount + increment;
    if (newCount >= 3 && newCount <= 5) {
      setPlayerCount(newCount);
      setPlayers(Array(newCount).fill(''));
    }
  };

  const updatePlayerName = (index, name) => {
    const newPlayers = [...players];
    newPlayers[index] = name;
    setPlayers(newPlayers);
  };

  const startGame = () => {
    if (players.some(name => !name)) return;
    
    // Sorteggio casuale del primo mazziere
    setFirstDealer(Math.floor(Math.random() * playerCount));
    
    // Mischia casualmente l'ordine delle mani
    const shuffledGames = [...initialGames]
      .sort(() => Math.random() - 0.5);
    
    setGames(shuffledGames);
    setGameStarted(true);
    setHandStartTime(Date.now());

    // Inizializza l'oggetto scores per tutti i giocatori
    const initialScores = {};
    players.forEach((_, index) => {
      initialScores[index] = '';
    });
    setScores(initialScores);
  };

  const getCurrentDealer = () => {
    const dealerIndex = (firstDealer + currentGame) % playerCount;
    return players[dealerIndex];
  };

  const submitScores = () => {
    // Verifica che tutti i punteggi siano stati inseriti
    if (Object.values(scores).some(score => score === '')) return;
    
    const handDuration = Math.floor((Date.now() - handStartTime) / 1000);
    
    const updatedGames = [...games];
    updatedGames[currentGame] = {
      ...updatedGames[currentGame],
      completed: true,
      scores: Object.fromEntries(
        Object.entries(scores).map(([key, value]) => [key, parseInt(value)])
      ),
      time: handDuration
    };

    setGames(updatedGames);
    
    // Resetta i punteggi per la prossima mano
    const resetScores = {};
    players.forEach((_, index) => {
      resetScores[index] = '';
    });
    setScores(resetScores);
    
    if (currentGame < games.length - 1) {
      setCurrentGame(currentGame + 1);
      setHandStartTime(Date.now());
      setElapsedTime(0);
    }
  };

  const calculateTotalScores = () => {
    const totals = {};
    players.forEach((_, index) => {
      totals[index] = 0;
    });

    games.forEach(game => {
      if (game.completed) {
        Object.entries(game.scores).forEach(([playerIndex, score]) => {
          totals[playerIndex] += score;
        });
      }
    });

    return totals;
  };

  const calculateTotalTime = () => {
    return games.reduce((total, game) => total + (game.time || 0), 0);
  };

  const getWinner = () => {
    const totals = calculateTotalScores();
    const minScore = Math.min(...Object.values(totals));
    const winners = Object.entries(totals)
      .filter(([_, score]) => score === minScore)
      .map(([index]) => players[index]);
    
    return winners.length > 1 ? `Pareggio tra ${winners.join(' e ')}` : winners[0];
  };

  const allGamesCompleted = games.every(game => game.completed);

  if (!gameStarted) {
    return (
      <div className="p-4 max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-bold text-center">Ramino Pokerato</h1>
            <div className="flex items-center justify-center gap-4 my-4">
              <Button 
                onClick={() => adjustPlayerCount(-1)}
                disabled={playerCount <= 3}
              >
                <Minus size={16} />
              </Button>
              <span className="text-lg font-medium">{playerCount} Giocatori</span>
              <Button 
                onClick={() => adjustPlayerCount(1)}
                disabled={playerCount >= 5}
              >
                <Plus size={16} />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {players.map((name, index) => (
              <div key={index} className="flex flex-col space-y-2">
                <label className="text-sm font-medium">Nome Giocatore {index + 1}:</label>
                <Input
                  value={name}
                  onChange={(e) => updatePlayerName(index, e.target.value)}
                  placeholder="Inserisci il nome"
                />
              </div>
            ))}

            <Button 
              className="w-full"
              onClick={startGame}
              disabled={players.some(name => !name)}
            >
              Inizia Partita
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <h1 className="text-2xl font-bold text-center">Ramino Pokerato</h1>
            {!allGamesCompleted && (
              <div className="text-center space-y-2">
                <p className="text-xl font-medium">{games[currentGame].name}</p>
                <p className="text-gray-600">{games[currentGame].description}</p>
              </div>
            )}
          </CardHeader>
          
          <CardContent>
            {!allGamesCompleted && (
              <>
                <Alert className="mb-4">
                  <AlertDescription className="flex justify-between items-center">
                    <span>Mazziere: <strong>{getCurrentDealer()}</strong></span>
                    <div className="flex items-center gap-2">
                      <Clock size={16} />
                      <span>{formatTime(elapsedTime)}</span>
                    </div>
                  </AlertDescription>
                </Alert>
                
                <div className="space-y-4">
                  {players.map((name, index) => (
                    <div key={index} className="flex flex-col space-y-2">
                      <label className="text-sm font-medium">Punti {name}:</label>
                      <Input
                        type="number"
                        value={scores[index]}
                        onChange={(e) => setScores({...scores, [index]: e.target.value})}
                        placeholder="Inserisci i punti"
                        min="0"
                      />
                    </div>
                  ))}

                  <Button 
                    className="w-full"
                    onClick={submitScores}
                    disabled={Object.values(scores).some(score => score === '')}
                  >
                    Conferma Punteggi
                  </Button>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold">Classifica Attuale</h2>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {Object.entries(calculateTotalScores())
                .sort(([,a], [,b]) => a - b)
                .map(([playerIndex, score]) => (
                  <div key={playerIndex} className="flex justify-between font-medium">
                    <span>{players[playerIndex]}</span>
                    <span>{score} punti</span>
                  </div>
                ))}
              <div className="text-sm text-gray-600 mt-4">
                Tempo totale: {formatTime(calculateTotalTime())}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold">Riepilogo Mani</h2>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {games.map((game) => (
                <div key={game.id} className="p-2 bg-gray-50 rounded">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-medium">{game.name}</span>
                    {game.completed && (
                      <span className="text-sm text-gray-600">
                        {formatTime(game.time)}
                      </span>
                    )}
                  </div>
                  {game.completed ? (
                    <div className="text-sm grid grid-cols-2 gap-2">
                      {Object.entries(game.scores).map(([playerIndex, score]) => (
                        <span key={playerIndex}>
                          {players[playerIndex]}: {score}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-sm text-gray-500">In attesa</span>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {allGamesCompleted && (
        <Card className="mt-6">
          <CardContent className="p-6">
            <div className="text-center">
              <h3 className="text-2xl font-bold mb-4">🏆 Partita Completata 🏆</h3>
              <div className="space-y-2">
                <p className="text-lg">Vincitore: <strong>{getWinner()}</strong></p>
                {Object.entries(calculateTotalScores())
                  .sort(([,a], [,b]) => a - b)
                  .map(([playerIndex, score]) => (
                    <p key={playerIndex}>
                      {players[playerIndex]}: {score} punti
                    </p>
                  ))}
                <p className="text-gray-600 mt-4">
                  Durata totale: {formatTime(calculateTotalTime())}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default RaminoGame;