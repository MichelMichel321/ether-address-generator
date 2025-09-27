import streamlit as st
import hashlib
from eth_keys import keys
from eth_utils import keccak
import secrets

# Configuration de la page
st.set_page_config(
    page_title="Création Adresse Ethereum",
    page_icon="⚡",
    layout="wide"
)

# Titre
st.title("⚡ TRAVAUX PRATIQUES")
st.header("Création d'une adresse Ethereum à partir d'une clé publique")
st.markdown("---")

# Initialisation de la session state
if 'private_key' not in st.session_state:
    st.session_state.private_key = None
    st.session_state.public_key = None
    st.session_state.keccak_hash = None
    st.session_state.eth_address = None

# Sidebar pour la génération
with st.sidebar:
    st.header("🔑 Génération de clés")
    if st.button("🎲 Générer une nouvelle paire de clés", type="primary", use_container_width=True):
        # Génération d'une clé privée aléatoire (256 bits = 32 octets)
        private_key_bytes = secrets.token_bytes(32)
        st.session_state.private_key = private_key_bytes.hex()
        
        # Création de l'objet clé privée
        private_key_obj = keys.PrivateKey(private_key_bytes)
        
        # Obtenir la clé publique (format non compressé, 64 octets)
        public_key_obj = private_key_obj.public_key
        st.session_state.public_key = public_key_obj.to_bytes().hex()
        
        # Calculer Keccak-256 de la clé publique
        keccak_hash = keccak(public_key_obj.to_bytes())
        st.session_state.keccak_hash = keccak_hash.hex()
        
        # Prendre les 20 derniers octets pour l'adresse
        eth_address = "0x" + keccak_hash.hex()[-40:]
        st.session_state.eth_address = eth_address
    
    st.markdown("---")
    st.info("💡 Ethereum utilise secp256k1 et Keccak-256")

# Affichage des étapes
if st.session_state.private_key:
    
    # Étape 1
    st.subheader("1️⃣ Générer une paire de clés avec ECDSA (secp256k1)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔒 Clé privée**")
        st.code(st.session_state.private_key, language="text")
        st.caption("Nombre aléatoire de 256 bits (32 octets)")
    
    with col2:
        st.markdown("**🔓 Clé publique**")
        st.code(st.session_state.public_key, language="text")
        st.caption("Point sur la courbe secp256k1 (64 octets, non compressée)")
    
    st.markdown("---")
    
    # Étape 2
    st.subheader("2️⃣ Appliquer Keccak-256 sur la clé publique")
    st.code(st.session_state.keccak_hash, language="text")
    st.caption("Hash Keccak-256 de la clé publique (32 octets)")
    
    st.markdown("---")
    
    # Étape 3
    st.subheader("3️⃣ Prendre les 20 derniers octets")
    last_20_bytes = st.session_state.keccak_hash[-40:]
    st.code(last_20_bytes, language="text")
    st.caption("Les 20 derniers octets du hash Keccak-256")
    
    st.markdown("---")
    
    # Étape 4
    st.subheader("4️⃣ Ajouter le préfixe 0x")
    st.markdown("**⚡ Adresse Ethereum finale**")
    st.code(st.session_state.eth_address, language="text")
    st.success("✅ Adresse Ethereum créée avec succès!")
    
    st.caption("Format: 0x + 20 octets (40 caractères hexadécimaux)")
    
    # Résumé dans un tableau
    st.markdown("---")
    st.subheader("📊 Résumé du processus")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        **Étapes:**
        1. Clé privée (256 bits)
        2. Clé publique ECDSA
        3. Hash Keccak-256
        4. 20 derniers octets
        5. Préfixe 0x
        """)
    
    with col2:
        st.markdown(f"""
        **Longueurs:**
        - Clé privée: {len(st.session_state.private_key)} caractères (32 octets)
        - Clé publique: {len(st.session_state.public_key)} caractères (64 octets)
        - Hash Keccak-256: {len(st.session_state.keccak_hash)} caractères (32 octets)
        - Adresse: {len(st.session_state.eth_address)} caractères (20 octets + 0x)
        """)
    
    # Téléchargement
    st.markdown("---")
    st.subheader("💾 Télécharger les informations")
    
    download_content = f"""ETHEREUM WALLET - TRAVAUX PRATIQUES
=====================================

1. CLÉ PRIVÉE (Private Key)
{st.session_state.private_key}

2. CLÉ PUBLIQUE (Public Key - Non compressée)
{st.session_state.public_key}

3. HASH KECCAK-256 DE LA CLÉ PUBLIQUE
{st.session_state.keccak_hash}

4. 20 DERNIERS OCTETS
{last_20_bytes}

5. ADRESSE ETHEREUM FINALE
{st.session_state.eth_address}

ALGORITHMES UTILISÉS:
- ECDSA avec courbe secp256k1
- Hash Keccak-256 (différent de SHA-256)

⚠️ ATTENTION: Ne partagez JAMAIS votre clé privée!
"""
    
    st.download_button(
        label="📥 Télécharger les détails complets",
        data=download_content,
        file_name="ethereum_address_creation.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # Comparaison Bitcoin vs Ethereum
    st.markdown("---")

else:
    # Instructions initiales
    st.info("👈 Cliquez sur le bouton dans la barre latérale pour générer une paire de clés")
    
    st.markdown("""
    ### 📚 Processus de création d'une adresse Ethereum
    
    **Étape 1:** Générer une paire de clés avec ECDSA (secp256k1)
    - Clé privée (256 bits)
    - Clé publique (point sur la courbe)
    
    **Étape 2:** Appliquer Keccak-256 sur la clé publique
    - Hash de la clé publique non compressée
    
    **Étape 3:** Prendre les 20 derniers octets
    - Les 40 derniers caractères hexadécimaux
    
    **Étape 4:** Ajouter le préfixe 0x
    - Format standard Ethereum
    
    **Résultat:** Une adresse Ethereum de 42 caractères
    """)
    
    # Exemple
    st.markdown("---")
    st.subheader("📝 Exemple d'adresse Ethereum")
    st.code("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0", language="text")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>⚡ Travaux Pratiques - Création d'adresse Ethereum</p>
    <p>🔐 Basé sur ECDSA (secp256k1) et Keccak-256</p>
</div>
""", unsafe_allow_html=True)