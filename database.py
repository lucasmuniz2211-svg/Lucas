import sqlite3
from datetime import datetime
import os

class AviatorDatabase:
    def __init__(self, db_name="aviator_data.db"):
        self.db_path = db_name
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela para registrar as velas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS velas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor REAL NOT NULL,
                tipo TEXT NOT NULL,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_crash BOOLEAN DEFAULT 0,
                sequencia_id INTEGER
            )
        ''')
        
        # Tabela para rastrear sequências
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sequencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_velas INTEGER DEFAULT 0,
                total_crashes INTEGER DEFAULT 0,
                intervalo_crashes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def adicionar_vela(self, valor, is_crash=False):
        """Adiciona uma vela ao banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tipo = "CRASH" if is_crash else "NORMAL"
        
        cursor.execute('''
            INSERT INTO velas (valor, tipo, is_crash)
            VALUES (?, ?, ?)
        ''', (valor, tipo, 1 if is_crash else 0))
        
        conn.commit()
        vela_id = cursor.lastrowid
        conn.close()
        
        return vela_id
    
    def adicionar_multiplas_velas(self, valores_lista):
        """Adiciona múltiplas velas de uma vez"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for valor in valores_lista:
            is_crash = valor == 0 or valor < 0.5  # Considera crash se valor muito baixo
            tipo = "CRASH" if is_crash else "NORMAL"
            
            cursor.execute('''
                INSERT INTO velas (valor, tipo, is_crash)
                VALUES (?, ?, ?)
            ''', (valor, tipo, 1 if is_crash else 0))
        
        conn.commit()
        conn.close()
    
    def obter_todas_velas(self):
        """Retorna todas as velas registradas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, valor, tipo, data_hora, is_crash 
            FROM velas 
            ORDER BY data_hora DESC
        ''')
        
        velas = cursor.fetchall()
        conn.close()
        
        return velas
    
    def obter_ultimas_velas(self, limite=50):
        """Retorna as últimas N velas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, valor, tipo, data_hora, is_crash 
            FROM velas 
            ORDER BY data_hora DESC 
            LIMIT ?
        ''', (limite,))
        
        velas = cursor.fetchall()
        conn.close()
        
        return list(reversed(velas))
    
    def obter_crashes(self):
        """Retorna apenas as velas que foram crash"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, valor, data_hora 
            FROM velas 
            WHERE is_crash = 1 
            ORDER BY data_hora DESC
        ''')
        
        crashes = cursor.fetchall()
        conn.close()
        
        return crashes
    
    def obter_estatisticas(self):
        """Calcula estatísticas dos dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM velas')
        total_velas = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM velas WHERE is_crash = 1')
        total_crashes = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(valor) FROM velas WHERE is_crash = 0')
        media_velas_normais = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(valor) FROM velas WHERE is_crash = 1')
        media_crashes = cursor.fetchone()[0]
        
        cursor.execute('SELECT MIN(valor), MAX(valor) FROM velas WHERE is_crash = 0')
        min_max = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_velas': total_velas,
            'total_crashes': total_crashes,
            'taxa_crash': (total_crashes / total_velas * 100) if total_velas > 0 else 0,
            'media_velas_normais': media_velas_normais,
            'media_crashes': media_crashes,
            'min_normal': min_max[0],
            'max_normal': min_max[1]
        }
    
    def limpar_dados(self):
        """Limpa todos os dados do banco (cuidado!)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM velas')
        cursor.execute('DELETE FROM sequencias')
        
        conn.commit()
        conn.close()
