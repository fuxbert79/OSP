/**
 * RMS E-Mail Spam-Filter Code
 *
 * Dieser Code kann in den bestehenden n8n Workflow "RMS-Email-Import"
 * als Code-Node eingefuegt werden.
 *
 * Position: Nach dem E-Mail-Parser Node, vor dem Create SharePoint Item Node
 */

// E-Mail-Daten aus dem vorherigen Node
const subject = $json.subject?.toLowerCase() || '';
const from = $json.from?.toLowerCase() || '';
const body = $json.bodyPreview?.toLowerCase() || '';

// Spam-Keywords (blockieren wenn vorhanden)
const spamKeywords = [
    'newsletter', 'unsubscribe', 'abmelden', 'werbung', 'angebot',
    'rabatt', 'gutschein', 'gewinnspiel', 'lottery', 'winner',
    'viagra', 'casino', 'bitcoin', 'crypto', 'investment opportunity',
    'click here', 'act now', 'limited time', 'free gift',
    'no obligation', 'risk free', 'satisfaction guaranteed',
    'special promotion', 'deal of the day', 'exclusive offer',
    'make money fast', 'work from home', 'earn extra cash'
];

// Whitelist-Domains (immer durchlassen)
const whitelistDomains = [
    'schneider-kabelsatzbau.de',
    // Lieferanten
    'wuerth.de', 'wuerth.com',
    'te.com', 'teconnectivity.com',
    'wago.com', 'weidmueller.com',
    'phoenix-contact.com', 'phoenixcontact.com',
    'molex.com',
    'amphenol.com',
    'jae.com',
    'yazaki.com',
    'sumitomo.com',
    'lapp.com', 'lappkabel.de',
    'helukabel.de', 'helukabel.com',
    // Kunden (bei Bedarf ergaenzen)
    'bosch.com', 'bosch.de',
    'zf.com',
    'continental.com',
    'schaeffler.com',
    'valeo.com'
];

// Blacklist-Domains (immer blockieren)
const blacklistDomains = [
    'spam.com', 'marketing.com', 'promo.com',
    'noreply-marketing.com', 'bulk-mail.com'
];

// Reklamations-Keywords (positiv - durchlassen)
const reklaKeywords = [
    'reklamation', 'beschwerde', 'mangel', 'fehler', 'defekt',
    'qualitaet', 'qualität', 'qa-', 'qm-',
    'ruecksendung', 'rücksendung', 'ersatz', 'gutschrift',
    'lieferschein', 'lieferung', 'beschaedigt', 'beschädigt',
    'falsch geliefert', 'fehlerhaft', 'nicht konform',
    'abweichung', 'maengel', 'mängel', 'beanstandung',
    '8d', '8-d', 'korrekturmassnahme', 'korrekturmaßnahme'
];

// Domain aus E-Mail-Adresse extrahieren
const fromDomain = from.split('@')[1]?.split('>')[0] || '';

// Pruefungen
const isWhitelisted = whitelistDomains.some(d => fromDomain.includes(d));
const isBlacklisted = blacklistDomains.some(d => fromDomain.includes(d));
const hasSpamKeyword = spamKeywords.some(kw => subject.includes(kw) || body.includes(kw));
const hasReklaKeyword = reklaKeywords.some(kw => subject.includes(kw) || body.includes(kw));

// Entscheidung
let isSpam = false;
let reason = '';
let confidence = 0;

if (isWhitelisted) {
    isSpam = false;
    reason = 'Whitelist: ' + fromDomain;
    confidence = 100;
} else if (isBlacklisted) {
    isSpam = true;
    reason = 'Blacklist: ' + fromDomain;
    confidence = 100;
} else if (hasReklaKeyword) {
    // Reklamations-Keywords haben Vorrang
    isSpam = false;
    reason = 'Reklamations-Keyword erkannt';
    confidence = 90;
} else if (hasSpamKeyword) {
    isSpam = true;
    reason = 'Spam-Keyword erkannt';
    confidence = 80;
} else {
    // Unbekannte Domain ohne eindeutige Keywords
    isSpam = false;
    reason = 'Keine Spam-Indikatoren gefunden';
    confidence = 60;
}

// Ergebnis zurueckgeben
return {
    ...$json,
    spamFilter: {
        isSpam: isSpam,
        reason: reason,
        confidence: confidence,
        fromDomain: fromDomain,
        checks: {
            whitelisted: isWhitelisted,
            blacklisted: isBlacklisted,
            hasSpamKeyword: hasSpamKeyword,
            hasReklaKeyword: hasReklaKeyword
        }
    }
};

/**
 * VERWENDUNG IN N8N:
 *
 * 1. Oeffne den Workflow "RMS-Email-Import"
 * 2. Fuege nach dem E-Mail-Parser einen neuen "Code" Node hinzu
 * 3. Kopiere diesen Code in den Node
 * 4. Fuege nach dem Code Node einen "IF" Node hinzu:
 *    - Bedingung: {{ $json.spamFilter.isSpam }} equals false
 *    - True-Branch: Weiter mit SharePoint Item erstellen
 *    - False-Branch: (Optional) Log Spam-Nachricht
 */
