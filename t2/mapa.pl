:- dynamic([
	m_inimigoD/2,
	m_inimigod/2,
	m_powerup/1,
	m_buraco/1,
	m_teleport/1,
	m_ouro/1
]).

m_powerup(p(1,12)).
m_buraco(p(2,11)).
m_teleport(p(4,11)).
m_ouro(p(9,11)).
m_buraco(p(10,10)).
m_inimigod(p(2,9),100).
m_buraco(p(7,9)).
m_buraco(p(4,8)).
m_inimigoD(p(11,8),100).
m_teleport(p(1,7)).
m_powerup(p(7,7)).
m_inimigoD(p(5,6),100).
m_buraco(p(10,6)).
m_ouro(p(3,5)).
m_buraco(p(3,3)).
m_teleport(p(7,3)).
m_buraco(p(11,3)).
m_powerup(p(2,2)).
m_buraco(p(5,2)).
m_inimigod(p(10,2),100).
m_ouro(p(11,2)).
m_teleport(p(10,1)).
