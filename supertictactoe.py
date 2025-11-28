import React, { useState } from 'react';
import { RefreshCw, Trophy } from 'lucide-react';

// --- Game Logic Helpers ---

const WINNING_COMBINATIONS = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // Cols
  [0, 4, 8], [2, 4, 6]             // Diagonals
];

// Returns { winner: 'X' | 'O', lineIndex: 0-7 } or null
const checkWinner = (squares) => {
  for (let i = 0; i < WINNING_COMBINATIONS.length; i++) {
    const [a, b, c] = WINNING_COMBINATIONS[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return { winner: squares[a], lineIndex: i };
    }
  }
  return null;
};

const checkDraw = (squares) => {
  return squares.every((square) => square !== null);
};

// --- Sub-Components ---

const StrikeLine = ({ lineIndex, colorClass, thickness = "h-1.5" }) => {
  // Map lineIndex to absolute positioning styles
  const getStyle = (index) => {
    const base = "absolute bg-current transform origin-center z-20 rounded-full shadow-sm pointer-events-none";
    
    // Adjust percentages to center lines perfectly in the 3x3 grid
    switch (index) {
      case 0: return `${base} left-2 right-2 top-[16.66%] -translate-y-1/2 h-1.5 w-[90%] scale-x-0 animate-strike-x`; // Row 1
      case 1: return `${base} left-2 right-2 top-[50%] -translate-y-1/2 h-1.5 w-[90%] scale-x-0 animate-strike-x`;    // Row 2
      case 2: return `${base} left-2 right-2 top-[83.33%] -translate-y-1/2 h-1.5 w-[90%] scale-x-0 animate-strike-x`; // Row 3
      case 3: return `${base} top-2 bottom-2 left-[16.66%] -translate-x-1/2 h-[90%] w-1.5 scale-y-0 animate-strike-y`; // Col 1
      case 4: return `${base} top-2 bottom-2 left-[50%] -translate-x-1/2 h-[90%] w-1.5 scale-y-0 animate-strike-y`;    // Col 2
      case 5: return `${base} top-2 bottom-2 left-[83.33%] -translate-x-1/2 h-[90%] w-1.5 scale-y-0 animate-strike-y`; // Col 3
      case 6: return `${base} top-1/2 left-0 right-0 h-1.5 -translate-y-1/2 rotate-45 scale-x-0 animate-strike-diag`;  // Diag 1
      case 7: return `${base} top-1/2 left-0 right-0 h-1.5 -translate-y-1/2 -rotate-45 scale-x-0 animate-strike-diag`; // Diag 2
      default: return "";
    }
  };

  return <div className={`${getStyle(lineIndex)} ${colorClass}`} />;
};

// --- Main Component ---

const UltimateTicTacToe = () => {
  // State
  const [bigGrid, setBigGrid] = useState(Array(9).fill(null).map(() => Array(9).fill(null)));
  
  // Track winners AND the winning line index for styling
  const [smallGridWinners, setSmallGridWinners] = useState(Array(9).fill(null)); 
  const [smallGridWinLines, setSmallGridWinLines] = useState(Array(9).fill(null));

  const [xIsNext, setXIsNext] = useState(true);
  const [nextTargetGrid, setNextTargetGrid] = useState(null);
  const [gameWinner, setGameWinner] = useState(null);
  const [gameWinLine, setGameWinLine] = useState(null);

  const currentPlayer = xIsNext ? 'X' : 'O';

  // Core Move Logic
  const handleSquareClick = (bigGridIndex, smallSquareIndex) => {
    if (gameWinner) return;
    if (nextTargetGrid !== null && nextTargetGrid !== bigGridIndex) return;
    if (bigGrid[bigGridIndex][smallSquareIndex] !== null) return;
    if (smallGridWinners[bigGridIndex] !== null) return;

    // Execute Move
    const newBigGrid = [...bigGrid];
    const newSmallGrid = [...newBigGrid[bigGridIndex]];
    newSmallGrid[smallSquareIndex] = currentPlayer;
    newBigGrid[bigGridIndex] = newSmallGrid;
    setBigGrid(newBigGrid);

    // Check Small Grid Win
    const newSmallGridWinners = [...smallGridWinners];
    const newSmallGridWinLines = [...smallGridWinLines];
    
    const smallWinResult = checkWinner(newSmallGrid);
    
    if (smallWinResult) {
      newSmallGridWinners[bigGridIndex] = smallWinResult.winner;
      newSmallGridWinLines[bigGridIndex] = smallWinResult.lineIndex;
      setSmallGridWinners(newSmallGridWinners);
      setSmallGridWinLines(newSmallGridWinLines);
    }

    // Check Big Game Win
    const bigWinResult = checkWinner(newSmallGridWinners);
    if (bigWinResult) {
      setGameWinner(bigWinResult.winner);
      setGameWinLine(bigWinResult.lineIndex);
      return; 
    }

    // Determine Next Target
    const targetGridIsWon = newSmallGridWinners[smallSquareIndex] !== null;
    const targetGridIsFull = checkDraw(newBigGrid[smallSquareIndex]);

    if (targetGridIsWon || targetGridIsFull) {
      setNextTargetGrid(null);
    } else {
      setNextTargetGrid(smallSquareIndex);
    }

    setXIsNext(!xIsNext);
  };

  const resetGame = () => {
    setBigGrid(Array(9).fill(null).map(() => Array(9).fill(null)));
    setSmallGridWinners(Array(9).fill(null));
    setSmallGridWinLines(Array(9).fill(null));
    setXIsNext(true);
    setNextTargetGrid(null);
    setGameWinner(null);
    setGameWinLine(null);
  };

  // --- Render Helpers ---

  const getPlayerColor = (player) => {
    if (player === 'X') return 'text-rose-400';
    if (player === 'O') return 'text-sky-400';
    return 'text-slate-400';
  };
  
  const getLineColor = (player) => {
    if (player === 'X') return 'bg-rose-400';
    if (player === 'O') return 'bg-sky-400';
    return 'bg-slate-400';
  };

  const getBgColor = (player) => {
    if (player === 'X') return 'bg-rose-100';
    if (player === 'O') return 'bg-sky-100';
    return 'bg-white';
  };

  return (
    <div className="min-h-screen bg-orange-50 font-sans flex flex-col items-center justify-center p-4 selection:bg-rose-200">
      
      {/* Styles for animations */}
      <style>{`
        @keyframes strike-x {
          0% { transform: translateY(-50%) scaleX(0); }
          100% { transform: translateY(-50%) scaleX(1); }
        }
        @keyframes strike-y {
          0% { transform: translateX(-50%) scaleY(0); }
          100% { transform: translateX(-50%) scaleY(1); }
        }
        @keyframes strike-diag {
          0% { transform: translateY(-50%) rotate(var(--tw-rotate)) scaleX(0); }
          100% { transform: translateY(-50%) rotate(var(--tw-rotate)) scaleX(1.2); }
        }
        .animate-strike-x { animation: strike-x 0.4s cubic-bezier(0.23, 1, 0.32, 1) forwards; }
        .animate-strike-y { animation: strike-y 0.4s cubic-bezier(0.23, 1, 0.32, 1) forwards; }
        .animate-strike-diag { animation: strike-diag 0.4s cubic-bezier(0.23, 1, 0.32, 1) forwards; }
      `}</style>

      {/* Header Area */}
      <div className="text-center mb-8 space-y-2">
        <h1 className="text-4xl md:text-5xl font-black text-slate-700 tracking-tight">
          <span className="text-rose-400">Super</span> Tic Tac Toe
        </h1>
        
        <div className="flex items-center justify-center gap-4 mt-4">
          <div className={`px-6 py-2 rounded-full text-lg font-bold shadow-sm transition-all duration-300 flex items-center gap-2
            ${gameWinner 
              ? 'bg-emerald-100 text-emerald-600' 
              : xIsNext ? 'bg-rose-100 text-rose-500 ring-2 ring-rose-200' : 'bg-white text-slate-400'
            }`}>
            {gameWinner === 'X' && <Trophy size={20} />}
            Player X
          </div>
          <div className={`px-6 py-2 rounded-full text-lg font-bold shadow-sm transition-all duration-300 flex items-center gap-2
            ${gameWinner 
              ? 'bg-emerald-100 text-emerald-600' 
              : !xIsNext ? 'bg-sky-100 text-sky-500 ring-2 ring-sky-200' : 'bg-white text-slate-400'
            }`}>
             {gameWinner === 'O' && <Trophy size={20} />}
            Player O
          </div>
        </div>

        {!gameWinner && (
          <p className="text-slate-500 font-medium animate-pulse mt-2">
            {nextTargetGrid === null 
              ? "Free Play! Choose any open grid." 
              : "Target Locked! Play in the highlighted grid."}
          </p>
        )}
      </div>

      {/* Game Board */}
      <div className="relative bg-white p-4 md:p-6 rounded-[2.5rem] shadow-xl ring-8 ring-white">
        
        {/* BIG GAME STRIKE LINE */}
        {gameWinner && gameWinLine !== null && (
          <div className="absolute inset-0 z-40 pointer-events-none p-4 md:p-6">
             <StrikeLine 
               lineIndex={gameWinLine} 
               colorClass={`${getLineColor(gameWinner)} opacity-90`} 
             />
          </div>
        )}

        {/* Game Winner Overlay (Text) */}
        {gameWinner && (
          <div className="absolute inset-0 z-50 rounded-[2.5rem] bg-white/40 backdrop-blur-[2px] flex flex-col items-center justify-center animate-in fade-in zoom-in duration-500 delay-300">
            <h2 className="text-6xl md:text-8xl font-black text-slate-800 mb-6 drop-shadow-2xl bg-white/80 px-8 py-4 rounded-3xl">
              <span className={getPlayerColor(gameWinner)}>{gameWinner}</span> Wins!
            </h2>
            <button 
              onClick={resetGame}
              className="px-8 py-3 bg-slate-800 text-white rounded-full font-bold shadow-lg hover:scale-105 hover:bg-slate-700 transition-all flex items-center gap-2"
            >
              <RefreshCw size={20} /> Play Again
            </button>
          </div>
        )}

        {/* 3x3 Large Grid */}
        <div className="grid grid-cols-3 gap-3 md:gap-4 relative z-0">
          {bigGrid.map((smallGrid, bigIndex) => {
            const isWinner = smallGridWinners[bigIndex];
            const winningLine = smallGridWinLines[bigIndex];
            
            // Active if: No game winner AND (It's a free turn OR this specific grid is the target)
            const isActive = !gameWinner && !isWinner && (nextTargetGrid === null || nextTargetGrid === bigIndex);
            
            return (
              <div 
                key={bigIndex} 
                className={`
                  relative w-24 h-24 md:w-32 md:h-32 lg:w-40 lg:h-40 
                  rounded-2xl flex flex-col items-center justify-center overflow-hidden
                  transition-all duration-300
                  ${isActive 
                    ? 'ring-4 ring-emerald-300 shadow-lg scale-105 z-10 bg-white' 
                    : 'bg-slate-50 ring-1 ring-slate-100 opacity-90'
                  }
                `}
              >
                {/* SMALL GRID STRIKE LINE & OVERLAY */}
                {isWinner && (
                  <>
                    {/* The Strike Line - Now z-10 (Lower) */}
                    <div className="absolute inset-0 pointer-events-none z-10 p-2">
                       {winningLine !== null && (
                         <StrikeLine 
                            lineIndex={winningLine} 
                            colorClass={getLineColor(isWinner)} 
                          />
                       )}
                    </div>
                    
                    {/* The Winner Overlay - Now z-20 (Higher) */}
                    <div className={`absolute inset-0 z-20 flex items-center justify-center ${
                      isWinner === 'X' ? 'bg-rose-50/80' : 'bg-sky-50/80'
                    } transition-colors duration-500`}>
                      <span className={`text-6xl md:text-7xl font-black opacity-30 ${getPlayerColor(isWinner)}`}>
                        {isWinner}
                      </span>
                    </div>
                  </>
                )}

                {/* The 3x3 Small Grid (Always rendered underneath) */}
                <div className="grid grid-cols-3 grid-rows-3 gap-1 md:gap-1.5 p-2 w-full h-full relative z-0">
                  {smallGrid.map((cell, smallIndex) => (
                    <button
                      key={smallIndex}
                      onClick={() => handleSquareClick(bigIndex, smallIndex)}
                      disabled={!isActive || cell !== null}
                      className={`
                        rounded-lg flex items-center justify-center text-lg md:text-xl font-bold transition-all
                        ${cell !== null ? getBgColor(cell) : 'bg-slate-100 hover:bg-slate-200'}
                        ${isActive && cell === null ? 'cursor-pointer' : 'cursor-default'}
                        ${!isActive ? 'opacity-50' : ''}
                      `}
                    >
                      <span className={getPlayerColor(cell)}>{cell}</span>
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Rules / Footer */}
      <div className="mt-8 flex gap-4">
        {!gameWinner && (
           <button 
           onClick={resetGame}
           className="p-3 bg-white text-slate-400 rounded-full hover:text-rose-400 hover:bg-rose-50 hover:shadow-md transition-all"
           title="Restart Game"
         >
           <RefreshCw size={24} />
         </button>
        )}
      </div>

      <div className="mt-6 text-slate-400 text-xs text-center max-w-md leading-relaxed">
        <strong>Rules:</strong> Playing in a small cell sends your opponent to the matching large grid. 
        If a target grid is full or won, you can play anywhere. Win 3 large grids in a row to win the game.
      </div>

    </div>
  );
};

export default UltimateTicTacToe;
