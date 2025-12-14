"""
OSP Revisions-Vergleich Artifact Pipeline für Open WebUI
=========================================================
Zeigt das Revisions-Vergleichs-Tool als interaktives Artifact im Chat an.

Version: 1.0
Autor: QM/KI-Manager (AL)
Datum: 2025-12-12
"""

import logging
from typing import List, Union, Generator

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Pipeline:
    """
    OSP Revisions-Vergleich als Chat-Artifact
    
    Ermöglicht den Vergleich von zwei Dokumentversionen direkt im Chat.
    Unterstützt: Excel, PDF, Word, Text/Markdown
    """
    
    def __init__(self):
        self.name = "OSP Revisions-Vergleich"
        self.id = "osp_revision_compare"
    
    async def on_startup(self):
        logger.info("🚀 OSP Revisions-Vergleich Pipeline gestartet")
    
    async def on_shutdown(self):
        logger.info("🛑 OSP Revisions-Vergleich Pipeline beendet")
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict
    ) -> Union[str, Generator]:
        """
        Gibt das Revisions-Vergleichs-Tool als React-Artifact zurück.
        """
        
        # React-Artifact mit dem Vergleichs-Tool
        artifact_code = '''
import React, { useState, useCallback } from 'react';
import { Upload, FileText, Table, File, RefreshCw, ChevronDown, ChevronUp, AlertCircle, CheckCircle } from 'lucide-react';

const RevisionCompare = () => {
  const [oldFile, setOldFile] = useState(null);
  const [newFile, setNewFile] = useState(null);
  const [oldContent, setOldContent] = useState('');
  const [newContent, setNewContent] = useState('');
  const [comparison, setComparison] = useState(null);
  const [isComparing, setIsComparing] = useState(false);
  const [stats, setStats] = useState({ added: 0, removed: 0, changed: 0, identical: 0 });
  
  // Datei-Typ Icons
  const getFileIcon = (fileName) => {
    if (!fileName) return <File className="w-5 h-5" />;
    const ext = fileName.split('.').pop().toLowerCase();
    if (['xlsx', 'xls', 'csv'].includes(ext)) return <Table className="w-5 h-5 text-green-600" />;
    if (['pdf'].includes(ext)) return <FileText className="w-5 h-5 text-red-500" />;
    if (['docx', 'doc'].includes(ext)) return <FileText className="w-5 h-5 text-blue-500" />;
    return <File className="w-5 h-5 text-gray-500" />;
  };
  
  // Text aus Datei lesen
  const readFileAsText = async (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = (e) => reject(e);
      reader.readAsText(file);
    });
  };
  
  // Datei-Handler
  const handleFileChange = async (e, isOld) => {
    const file = e.target.files[0];
    if (!file) return;
    
    try {
      const content = await readFileAsText(file);
      if (isOld) {
        setOldFile(file);
        setOldContent(content);
      } else {
        setNewFile(file);
        setNewContent(content);
      }
    } catch (err) {
      console.error('Fehler beim Lesen:', err);
    }
  };
  
  // Vergleich durchführen
  const compareFiles = useCallback(() => {
    if (!oldContent || !newContent) return;
    
    setIsComparing(true);
    
    const oldLines = oldContent.split('\\n');
    const newLines = newContent.split('\\n');
    const maxLines = Math.max(oldLines.length, newLines.length);
    
    const results = [];
    const newStats = { added: 0, removed: 0, changed: 0, identical: 0 };
    
    for (let i = 0; i < maxLines; i++) {
      const oldLine = (oldLines[i] || '').trim();
      const newLine = (newLines[i] || '').trim();
      
      if (oldLine === newLine) {
        if (oldLine) {
          newStats.identical++;
          results.push({ line: i + 1, type: 'identical', old: oldLine, new: newLine });
        }
      } else if (oldLine && !newLine) {
        newStats.removed++;
        results.push({ line: i + 1, type: 'removed', old: oldLine, new: '' });
      } else if (!oldLine && newLine) {
        newStats.added++;
        results.push({ line: i + 1, type: 'added', old: '', new: newLine });
      } else {
        newStats.changed++;
        results.push({ line: i + 1, type: 'changed', old: oldLine, new: newLine });
      }
    }
    
    setStats(newStats);
    setComparison(results.filter(r => r.type !== 'identical'));
    setIsComparing(false);
  }, [oldContent, newContent]);
  
  // Reset
  const resetAll = () => {
    setOldFile(null);
    setNewFile(null);
    setOldContent('');
    setNewContent('');
    setComparison(null);
    setStats({ added: 0, removed: 0, changed: 0, identical: 0 });
  };
  
  // Farb-Klassen
  const getRowClass = (type) => {
    switch (type) {
      case 'added': return 'bg-green-50 border-l-4 border-green-500';
      case 'removed': return 'bg-red-50 border-l-4 border-red-500';
      case 'changed': return 'bg-yellow-50 border-l-4 border-yellow-500';
      default: return '';
    }
  };
  
  const getTypeLabel = (type) => {
    switch (type) {
      case 'added': return '➕ Hinzugefügt';
      case 'removed': return '➖ Entfernt';
      case 'changed': return '✏️ Geändert';
      default: return '';
    }
  };
  
  return (
    <div className="w-full max-w-6xl mx-auto p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b-2 border-orange-400 pb-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl font-bold text-orange-500">OSP</span>
          <span className="text-xl font-semibold text-gray-700">Revisions-Vergleich</span>
          <span className="bg-blue-600 text-white px-2 py-1 rounded text-xs font-medium">v2.2</span>
        </div>
        <button 
          onClick={resetAll}
          className="flex items-center gap-2 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition"
        >
          <RefreshCw className="w-4 h-4" />
          Zurücksetzen
        </button>
      </div>
      
      {/* Upload-Bereich */}
      <div className="grid grid-cols-2 gap-4">
        {/* Original */}
        <div className="border-2 border-dashed border-blue-300 rounded-xl p-6 hover:border-blue-500 transition bg-blue-50">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="font-semibold text-gray-700">ORIGINAL (Alte Version)</span>
          </div>
          <label className="flex flex-col items-center cursor-pointer">
            <Upload className="w-12 h-12 text-blue-400 mb-2" />
            <span className="text-sm text-gray-500">Datei hier ablegen oder klicken</span>
            <input 
              type="file" 
              className="hidden" 
              onChange={(e) => handleFileChange(e, true)}
              accept=".txt,.md,.csv,.json"
            />
          </label>
          {oldFile && (
            <div className="mt-4 flex items-center gap-2 p-2 bg-white rounded border">
              {getFileIcon(oldFile.name)}
              <span className="text-sm font-medium">{oldFile.name}</span>
              <CheckCircle className="w-4 h-4 text-green-500 ml-auto" />
            </div>
          )}
        </div>
        
        {/* Revision */}
        <div className="border-2 border-dashed border-orange-300 rounded-xl p-6 hover:border-orange-500 transition bg-orange-50">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span className="font-semibold text-gray-700">REVISION (Neue Version)</span>
          </div>
          <label className="flex flex-col items-center cursor-pointer">
            <Upload className="w-12 h-12 text-orange-400 mb-2" />
            <span className="text-sm text-gray-500">Datei hier ablegen oder klicken</span>
            <input 
              type="file" 
              className="hidden" 
              onChange={(e) => handleFileChange(e, false)}
              accept=".txt,.md,.csv,.json"
            />
          </label>
          {newFile && (
            <div className="mt-4 flex items-center gap-2 p-2 bg-white rounded border">
              {getFileIcon(newFile.name)}
              <span className="text-sm font-medium">{newFile.name}</span>
              <CheckCircle className="w-4 h-4 text-green-500 ml-auto" />
            </div>
          )}
        </div>
      </div>
      
      {/* Vergleich-Button */}
      {oldContent && newContent && (
        <div className="flex justify-center">
          <button
            onClick={compareFiles}
            disabled={isComparing}
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-blue-800 transition shadow-lg disabled:opacity-50"
          >
            {isComparing ? '⏳ Vergleiche...' : '🔍 Dokumente vergleichen'}
          </button>
        </div>
      )}
      
      {/* Statistik */}
      {comparison && (
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-green-100 p-4 rounded-xl text-center">
            <div className="text-2xl font-bold text-green-700">{stats.added}</div>
            <div className="text-sm text-green-600">Hinzugefügt</div>
          </div>
          <div className="bg-red-100 p-4 rounded-xl text-center">
            <div className="text-2xl font-bold text-red-700">{stats.removed}</div>
            <div className="text-sm text-red-600">Entfernt</div>
          </div>
          <div className="bg-yellow-100 p-4 rounded-xl text-center">
            <div className="text-2xl font-bold text-yellow-700">{stats.changed}</div>
            <div className="text-sm text-yellow-600">Geändert</div>
          </div>
          <div className="bg-gray-100 p-4 rounded-xl text-center">
            <div className="text-2xl font-bold text-gray-700">{stats.identical}</div>
            <div className="text-sm text-gray-600">Identisch</div>
          </div>
        </div>
      )}
      
      {/* Ergebnis-Anzeige */}
      {comparison && comparison.length > 0 && (
        <div className="border rounded-xl overflow-hidden">
          <div className="bg-gray-800 text-white px-4 py-3 font-semibold">
            📋 Änderungen ({comparison.length})
          </div>
          <div className="max-h-96 overflow-auto">
            {comparison.map((item, idx) => (
              <div key={idx} className={`p-4 border-b ${getRowClass(item.type)}`}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-mono bg-gray-200 px-2 py-1 rounded">
                    Zeile {item.line}
                  </span>
                  <span className="text-sm font-medium">
                    {getTypeLabel(item.type)}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Original:</div>
                    <div className="bg-white p-2 rounded border font-mono text-xs">
                      {item.old || <em className="text-gray-400">(leer)</em>}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Revision:</div>
                    <div className="bg-white p-2 rounded border font-mono text-xs">
                      {item.new || <em className="text-gray-400">(leer)</em>}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {comparison && comparison.length === 0 && (
        <div className="text-center p-8 bg-green-50 rounded-xl border-2 border-green-200">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-green-700">Keine Unterschiede gefunden</h3>
          <p className="text-green-600">Die Dokumente sind identisch!</p>
        </div>
      )}
      
      {/* Hinweis */}
      <div className="text-xs text-gray-500 text-center p-2 bg-gray-50 rounded">
        💡 Unterstützt: .txt, .md, .csv, .json | Für Excel/Word/PDF: Vollversion nutzen
      </div>
    </div>
  );
};

export default RevisionCompare;
'''
        
        # Markdown mit eingebettetem Artifact
        response = f"""# 📄 OSP Revisions-Vergleich

Das Revisions-Vergleichs-Tool ist jetzt verfügbar. Lade zwei Dokumente hoch um sie zu vergleichen.

**Unterstützte Formate in dieser Version:**
- Text-Dateien (.txt, .md)
- CSV-Dateien (.csv)
- JSON-Dateien (.json)

> 💡 **Tipp:** Für Excel, Word und PDF nutze die [Vollversion (HTML)]({self._get_full_version_path()})

---

```artifact
{artifact_code}
```
"""
        
        return response
    
    def _get_full_version_path(self) -> str:
        """Gibt den Pfad zur Vollversion zurück"""
        return "file:///C:/Users/andreas.loehr.SCHNEIDER/OneDrive%20-%20Rainer%20Schneider%20Kabelsatzbau%20und%20Konfektion/claude/OSP_Revisions_Vergleich.html"


# Pipeline-Instanz für Open WebUI
pipeline = Pipeline()
