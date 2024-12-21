import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Clock, Plus, Minus, Trophy, User, Users, PlayCircle, Award, Timer, Crown, Star, Heart, Shuffle, List, Save, RotateCcw } from 'lucide-react';
import ReactConfetti from 'react-confetti';

const STORAGE_KEY = 'raminoGameState';

const RaminoGame = () => {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });
  const [gameStarted, setGameStarted] = useState(false);
  const [playerCount, setPlayerCount] = useState(2);
  const [players, setPlayers] = useState(Array(2).fill(''));
  const [firstDealer, setFirstDealer] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [handStartTime, setHandStartTime] = useState(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [gameMode, setGameMode] = useState('classic');
  
  const initialGames = [
    { id: 1, name: 'Coppia', description: 'Coppia figurata (J, Q, K, A)', completed: false, scores: {}, time: 0, icon: '👥' },
    { id: 2, name: 'Doppia Coppia', description: 'Doppia coppia, una figurata', completed: false, scores: {}, time: 0, icon: '👥👥' },
    { id: 3, name: 'Tris', description: 'Qualsiasi tris', completed: false, scores: {}, time: 0, icon: '🎲' },
    { id: 4, name: 'Full', description: 'Qualsiasi full', completed: false, scores: {}, time: 0, icon: '🎰' },
    { id: 5, name: 'Scala 40', description: 'Scala da 40 punti esatti', completed: false, scores: {}, time: 0, icon: '📈' },
    { id: 6, name: 'Poker', description: 'Qualsiasi poker', completed: false, scores: {}, time: 0, icon: '♠️' },
    { id: 7, name: 'Scala Colore', description: 'Scala di 5 carte dello stesso seme', completed: false, scores: {}, time: 0, icon: '🌈' },
    { id: 8, name: 'Chiusura in Mano', description: 'Apertura = chiusura senza scarto', completed: false, scores: {}, time: 0, icon: '🎯' }
  ];

  const [games, setGames] = useState([]);
  const [currentGame, setCurrentGame] = useState(0);
  const [scores, setScores] = useState({});

  // Carica lo stato salvato all'avvio
  useEffect(() => {
    const savedState = localStorage.getItem(STORAGE_KEY);
    if (savedState) {
      const state = JSON.parse(savedState);
      setGameStarted(state.gameStarted);
      setPlayerCount(state.playerCount);
      setPlayers(state.players);
      setFirstDealer(state.firstDealer);
      setGameMode(state.gameMode);
      setGames(state.games);
      setCurrentGame(state.currentGame);
      setScores(state.scores);
      
      if (state.gameStarted && !state.games.every(game => game.completed)) {
        setHandStartTime(Date.now() - (state.elapsedTime * 1000));
        setElapsedTime(state.elapsedTime);
      }
    }
  }, []);

  // Salva lo stato quando cambia qualcosa
  useEffect(() => {
    if (gameStarted) {
      const stateToSave = {
        gameStarted,
        playerCount,
        players,
        firstDealer,
        elapsedTime,
        gameMode,
        games,
        currentGame,
        scores
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(stateToSave));
    }
  }, [gameStarted, playerCount, players, firstDealer, elapsedTime, gameMode, games, currentGame, scores]);

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    let timer;
    if (gameStarted && !allGamesCompleted && handStartTime) {
      timer = setInterval(() => {
        setElapsedTime(Math.floor((Date.now() - handStartTime) / 1000));
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [gameStarted, handStartTime]);

  useEffect(() => {
    if (showConfetti) {
      const timer = setTimeout(() => {
        setShowConfetti(false);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [showConfetti]);

  const resetGame = () => {
    localStorage.removeItem(STORAGE_KEY);
    window.location.reload();
  };
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const adjustPlayerCount = (increment) => {
    const newCount = playerCount + increment;
    if (newCount >= 2 && newCount <= 5) {
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
    setFirstDealer(Math.floor(Math.random() * playerCount));
    
    const gamesList = gameMode === 'random' 
      ? [...initialGames].sort(() => Math.random() - 0.5)
      : [...initialGames];
    
    setGames(gamesList);
    setGameStarted(true);
    setHandStartTime(Date.now());
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
    
    const resetScores = {};
    players.forEach((_, index) => {
      resetScores[index] = '';
    });
    setScores(resetScores);
    
    if (currentGame < games.length - 1) {
      setCurrentGame(currentGame + 1);
      setHandStartTime(Date.now());
      setElapsedTime(0);
    } else {
      setShowConfetti(true);
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

  const getScoreColor = (score) => {
    if (!score) return 'text-gray-600';
    if (score <= 50) return 'text-green-600';
    if (score <= 100) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRankIcon = (rank) => {
    switch(rank) {
      case 0: return <Crown className="text-yellow-500" size={24} />;
      case 1: return <Star className="text-gray-500" size={24} />;
      case 2: return <Heart className="text-orange-500" size={24} />;
      default: return null;
    }
  };
  if (!gameStarted) {
    return (
      <div className="p-4 max-w-2xl mx-auto min-h-screen bg-gradient-to-b from-blue-50 to-white">
        <Card className="backdrop-blur-lg bg-white/90 shadow-xl">
          <CardHeader className="space-y-4">
            <div className="text-center space-y-2">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                🎴 Ramino Pokerato
              </h1>
              <p className="text-gray-600">Il classico gioco di carte in versione moderna</p>
            </div>

            {localStorage.getItem(STORAGE_KEY) && (
              <Alert className="bg-yellow-50 border-yellow-200">
                <AlertDescription className="flex justify-between items-center">
                  <span>C'è una partita in corso salvata</span>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={resetGame}
                      className="flex items-center gap-2"
                    >
                      <RotateCcw size={16} />
                      Nuova Partita
                    </Button>
                  </div>
                </AlertDescription>
              </Alert>
            )}

            <div className="flex justify-center gap-4 my-6">
              <Button
                onClick={() => setGameMode('classic')}
                variant={gameMode === 'classic' ? 'default' : 'outline'}
                className="flex items-center gap-2 px-6 py-4 transition-all hover:scale-105"
              >
                <List size={20} />
                Modalità Classica
              </Button>
              <Button
                onClick={() => setGameMode('random')}
                variant={gameMode === 'random' ? 'default' : 'outline'}
                className="flex items-center gap-2 px-6 py-4 transition-all hover:scale-105"
              >
                <Shuffle size={20} />
                Modalità Random
              </Button>
            </div>
            
            <div className="flex items-center justify-center gap-4 my-6">
              <Button 
                onClick={() => adjustPlayerCount(-1)}
                disabled={playerCount <= 2}
                variant="outline"
                className="w-12 h-12 rounded-full transition-all hover:scale-105"
              >
                <Minus size={20} />
              </Button>
              <div className="flex items-center gap-2 min-w-[100px] justify-center">
                <Users size={24} className="text-blue-600" />
                <span className="text-xl font-medium">{playerCount}</span>
              </div>
              <Button 
                onClick={() => adjustPlayerCount(1)}
                disabled={playerCount >= 5}
                variant="outline"
                className="w-12 h-12 rounded-full transition-all hover:scale-105"
              >
                <Plus size={20} />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <Alert className="bg-blue-50 border-blue-200">
              <AlertDescription>
                <div className="flex items-center gap-2">
                  {gameMode === 'classic' ? <List size={20} /> : <Shuffle size={20} />}
                  <span>
                    {gameMode === 'classic' 
                      ? 'Le mani verranno giocate nell\'ordine tradizionale' 
                      : 'Le mani verranno mescolate in ordine casuale'}
                  </span>
                </div>
              </AlertDescription>
            </Alert>

            {players.map((name, index) => (
              <div key={index} className="transform transition-all hover:scale-[1.02]">
                <div className="flex items-center gap-3 mb-2">
                  <User size={20} className="text-blue-600" />
                  <label className="text-lg font-medium text-gray-700">
                    Giocatore {index + 1}
                  </label>
                </div>
                <Input
                  value={name}
                  onChange={(e) => updatePlayerName(index, e.target.value)}
                  placeholder="Inserisci il nome"
                  className="h-12 text-lg border-2 focus:ring-2 focus:ring-blue-200"
                />
              </div>
            ))}

            <Button 
              className="w-full h-14 text-lg mt-8 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-[1.02]"
              onClick={startGame}
              disabled={players.some(name => !name)}
            >
              <PlayCircle size={24} className="mr-2" />
              Inizia Partita
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-4 max-w-6xl mx-auto min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {showConfetti && <ReactConfetti width={windowSize.width} height={windowSize.height} />}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="md:col-span-2 backdrop-blur-lg bg-white/90 shadow-xl">
          <CardHeader>
            <div className="flex justify-between items-center mb-4">
              <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                🎴 Ramino Pokerato
              </h1>
              <Button
                variant="outline"
                size="sm"
                onClick={resetGame}
                className="flex items-center gap-2"
              >
                <RotateCcw size={16} />
                Nuova Partita
              </Button>
            </div>
            {!allGamesCompleted && (
              <div className="text-center space-y-3 bg-white p-6 rounded-xl shadow-inner">
                <div className="flex items-center justify-center gap-2">
                  <span className="text-3xl">{games[currentGame].icon}</span>
                  <p className="text-2xl font-medium text-blue-600">{games[currentGame].name}</p>
                </div>
                <p className="text-gray-600">{games[currentGame].description}</p>
              </div>
            )}
          </CardHeader>
          
          <CardContent>
            {!allGamesCompleted && (
              <>
                <Alert className="mb-6 bg-white border-2 border-blue-200 shadow-sm">
                  <AlertDescription className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <Award size={20} className="text-blue-600" />
                      <span>Mazziere: <strong className="text-blue-600">{getCurrentDealer()}</strong></span>
                    </div>
                    <div className="flex items-center gap-2 bg-blue-50 px-4 py-2 rounded-full shadow-inner">
                      <Timer size={20} className="text-blue-600" />
                      <span className="font-medium">{formatTime(elapsedTime)}</span>
                    </div>
                  </AlertDescription>
                </Alert>
                
                <div className="grid gap-4">
                  {players.map((name, index) => (
                    <div key={index} className="bg-white p-6 rounded-xl shadow-sm border-2 border-gray-100 hover:border-blue-200 transition-all">
                      <div className="flex justify-between items-center mb-3">
                        <label className="text-lg font-medium text-gray-700">
                          {name}
                        </label>
                        <span className={`font-medium ${getScoreColor(scores[index])}`}>
                          {scores[index] ? `${scores[index]} punti` : ''}
                        </span>
                      </div>
                      <Input
                        type="number"
                        value={scores[index]}
                        onChange={(e) => setScores({...scores, [index]: e.target.value})}
                        placeholder="Inserisci i punti"
                        min="0"
                        className="h-12 text-lg border-2 focus:ring-2 focus:ring-blue-200"
                      />
                    </div>
                  ))}

                  <Button 
                    className="w-full h-12 text-lg mt-4 bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 transform hover:scale-[1.02] transition-all"
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

        <Card className="backdrop-blur-lg bg-white/90 shadow-xl">
          <CardHeader>
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Trophy size={24} className="text-yellow-500" />
              Classifica Attuale
            </h2>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(calculateTotalScores())
                .sort(([,a], [,b]) => a - b)
                .map(([playerIndex, score], rank) => (
                  <div 
                    key={playerIndex} 
                    className={`flex justify-between items-center p-4 rounded-xl border-2 transition-all hover:scale-[1.02] ${
                      rank === 0 ? 'bg-yellow-50 border-yellow-200' :
                      rank === 1 ? 'bg-gray-50 border-gray-200' :
                      rank === 2 ? 'bg-orange-50 border-orange-200' :
                      'bg-blue-50 border-blue-200'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      {getRankIcon(rank)}
                      <span className="font-medium">{players[playerIndex]}</span>
                    </div>
                    <span className="font-bold">{score} punti</span>
                  </div>
                ))}
              <div className="flex items-center justify-between pt-4 px-4 text-gray-600 bg-gray-50 rounded-xl">
                <Clock size={20} />
                <span className="font-medium">{formatTime(calculateTotalTime())}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="backdrop-blur-lg bg-white/90 shadow-xl">
          <CardHeader>
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Award size={24} className="text-blue-500" />
              Riepilogo Mani
            </h2>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {games.map((game) => (
                <div key={game.id} className={`p-4 rounded-xl border-2 transition-all hover:scale-[1.01] ${
                  game.completed ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
                }`}>
                  <div className="flex justify-between items-center mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{game.icon}</span>
                      <span className="font-medium">{game.name}</span>
                    </div>
                    {game.completed && (
                      <div className="flex items-center gap-1 text-gray-600 bg-white px-3 py-1 rounded-full shadow-inner">
                        <Clock size={16} />
                        <span>{formatTime(game.time)}</span>
                      </div>
                    )}
                  </div>
                  {game.completed ? (
                    <div className="grid grid-cols-2 gap-3 mt-2">
                      {Object.entries(game.scores).map(([playerIndex, score]) => (
                        <div key={playerIndex} className="flex justify-between bg-white p-2 rounded-lg shadow-sm">
                          <span className="text-gray-600">{players[playerIndex]}</span>
                          <span className={getScoreColor(score)}>{score}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <span className="text-sm text-gray-500 italic flex items-center gap-2">
                      <Timer size={16} />
                      In attesa
                    </span>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {allGamesCompleted && (
        <Card className="mt-6 backdrop-blur-lg bg-gradient-to-br from-yellow-100 to-orange-100 shadow-xl border-2 border-yellow-200">
          <CardContent className="p-8">
            <div className="text-center space-y-8">
              <div className="space-y-4">
                <h3 className="text-4xl font-bold bg-gradient-to-r from-yellow-600 to-orange-600 bg-clip-text text-transparent">
                  🏆 Partita Completata 🏆
                </h3>
                <div className="inline-block bg-white px-8 py-4 rounded-full shadow-lg border-2 border-yellow-200">
                  <p className="text-2xl text-yellow-800">
                    Vincitore: <strong>{getWinner()}</strong>
                  </p>
                </div>
              </div>

              <div className="grid gap-3 max-w-md mx-auto">
                {Object.entries(calculateTotalScores())
                  .sort(([,a], [,b]) => a - b)
                  .map(([playerIndex, score], index) => (
                    <div 
                      key={playerIndex}
                      className={`flex justify-between items-center p-4 rounded-xl shadow-md backdrop-blur-md transition-all hover:scale-[1.02] ${
                        index === 0 ? 'bg-yellow-100/90 border-2 border-yellow-200' :
                        index === 1 ? 'bg-gray-100/90 border-2 border-gray-200' :
                        index === 2 ? 'bg-orange-100/90 border-2 border-orange-200' :
                        'bg-blue-100/90 border-2 border-blue-200'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        {getRankIcon(index)}
                        <span className="font-medium">{players[playerIndex]}</span>
                      </div>
                      <span className="font-bold">{score} punti</span>
                    </div>
                  ))}
              </div>

              <div className="flex items-center justify-center gap-2 text-gray-600 bg-white px-6 py-3 rounded-full shadow-inner mx-auto w-fit">
                <Clock size={20} />
                <span className="font-medium">
                  Durata totale: {formatTime(calculateTotalTime())}
                </span>
              </div>

              <Button
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg py-6 px-8 rounded-xl shadow-lg transform hover:scale-[1.02] transition-all"
                onClick={resetGame}
              >
                Nuova Partita
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default RaminoGame;