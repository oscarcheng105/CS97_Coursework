import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props){
    return (
        <button className="square" onClick={() => props.onClick()}>
            {props.value}
        </button>
    );
  }

function calculateWinner(squares){
    const lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
      ];
    for (let i = 0; i < lines.length; i++) {
        const [a, b, c] = lines[i];
        if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
            return squares[a];
        }
    }
    return null;
}
  
  class Board extends React.Component {
    renderSquare(i) {
      return <Square 
                    value = {this.props.squares[i]}
                    onClick={() => this.props.onClick(i)}/>;
    }
  
    render() {
      return (
        <div>
          <div className="board-row">
            {this.renderSquare(0)}
            {this.renderSquare(1)}
            {this.renderSquare(2)}
          </div>
          <div className="board-row">
            {this.renderSquare(3)}
            {this.renderSquare(4)}
            {this.renderSquare(5)}
          </div>
          <div className="board-row">
            {this.renderSquare(6)}
            {this.renderSquare(7)}
            {this.renderSquare(8)}
          </div>
        </div>
      );
    }
  }
  
  class Game extends React.Component {

    constructor(props)
    {
        super(props);
        this.state = {
            squares: Array(9).fill(null),
            xIsNext:true,
            stepNumber:0,
            movePiece: false,
            prevSqr: null,
        }
    }

    handleRestart()
    {
        this.setState({
            squares: Array(9).fill(null),
            xIsNext: true,
            stepNumber: 0,
            movePiece: false,
            prevSqr: null,
        });
    }

    handleClick(i)
    {   
        let squares = this.state.squares.slice();
        let player = this.state.xIsNext ? "X" : "O";
        let xIsNext = this.state.xIsNext;
        let stepNumber = this.state.stepNumber;
        let movePiece = this.state.movePiece;
        let prevSqr = this.state.prevSqr;
        if(this.state.stepNumber < 6)
        {
            if(calculateWinner(squares) || squares[i])
                return;
            squares[i] = player;
            xIsNext = !xIsNext;
            stepNumber += 1;
        }
        else
        {
            if( calculateWinner(squares) ||
                (squares[i] !== player && !movePiece) ||
                (movePiece && squares[i] !== null))
                return
            else if(squares[i] === player && !movePiece)
            {
                squares[i] = null;
                movePiece = !movePiece;
                prevSqr = i;
            }
            else if(movePiece && squares[i] === null)
            {
                let center = squares[4];
                squares[i] = player;
                if(center === player && !calculateWinner(squares) && i !== prevSqr)
                    squares[i] = null;
                else
                {
                movePiece = !movePiece;
                if(i !== prevSqr)
                    xIsNext = !xIsNext;
                prevSqr = null
                }
            }         
        }
        this.setState({
            squares: squares,
            xIsNext: xIsNext,
            stepNumber: stepNumber,
            movePiece: movePiece,
            prevSqr: prevSqr,
        });
    }

    render() {
        let winner = calculateWinner(this.state.squares)
        let status;
        if (winner) 
            status = 'Winner: ' + winner;
        else 
            status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
        return (
            <div className="game">
                <div className="game-board">
                    <Board 
                    squares = {this.state.squares}
                    onClick={(i) => {this.handleClick(i)}} />
                </div>
                <div className="game-info">
                    <div className="status">{status}</div>
                    <button onClick={()=>{this.handleRestart()}}>Restart</button>
                </div>
            </div>
        );
    }
  }
  
  // ========================================
  
  ReactDOM.render(
    <Game />,
    document.getElementById('root')
  );