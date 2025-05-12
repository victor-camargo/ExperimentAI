import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowLeft, faChevronDown, faChevronUp } from '@fortawesome/free-solid-svg-icons'
import './App.css'
import axios from 'axios'

function App() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [result, setResult] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [showResult, setShowResult] = useState(false)
  const [backendResponse, setBackendResponse] = useState(null)
  const [expandedItems, setExpandedItems] = useState({})

  const mockEquipments = [
    "Béquer de vidro - Usado para medição e mistura de líquidos em laboratório",
    "Microscópio óptico - Equipamento para observação de amostras microscópicas",
    "Pipeta volumétrica - Instrumento para medição precisa de volumes líquidos",
    "Erlenmeyer - Frasco cônico utilizado em titulações e aquecimento de soluções",
    "Bureta - Instrumento de vidro usado para dispensar volumes precisos de líquidos"
  ]

  // Função para alternar a expansão de um item
  const toggleExpand = (itemId) => {
    setExpandedItems(prev => ({
      ...prev,
      [itemId]: !prev[itemId]
    }));
  };

  const handleFileChange = (event) => {
    setShowResult(false)
    setIsProcessing(true)
    const file = event.target.files[0]
    if (!file) {
      setIsProcessing(false)
      return
    }

    const stripBase64Prefix = (base64String) => {
      return base64String.split(',')[1]
    };

    const convertToBase64 = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = (error) => reject(error)
      })
    }

    const convertBase64ToImage = (base64String, fileName) => {
      
      const byteString = atob(base64String);
      const mimeString = "image/png";
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const uintArray = new Uint8Array(arrayBuffer);

      for (let i = 0; i < byteString.length; i++) {
        uintArray[i] = byteString.charCodeAt(i);
      }

      const blob = new Blob([arrayBuffer], { type: mimeString });
      return new File([blob], fileName, { type: mimeString });
    };

    const sendImageToEndpoint = async (base64Image) => {
      try {
      const response = await axios.post('http://localhost/api/experimentai/vss', {
        image_b64: stripBase64Prefix(base64Image),
      })
      setBackendResponse(response.data)
      console.log('Resposta do servidor:', response.data)
      } catch (error) {
      console.error('Erro ao enviar imagem para o endpoint:', error)
      }
    }

      convertToBase64(file)
      .then((base64) => {
        sendImageToEndpoint(base64)
      })
      .catch((error) => {
        console.error('Erro ao converter imagem para base64:', error)
      })

    setSelectedImage(URL.createObjectURL(file))
    
    setShowResult(true)
    
    setTimeout(() => {
      const randomIndex = Math.floor(Math.random() * mockEquipments.length)
      setResult(mockEquipments[randomIndex])
      setIsProcessing(false)
    }, 1500)
  }

  const handleBack = () => {
    setShowResult(false)
    setSelectedImage(null)
    setResult('')
  }

  if (showResult) {
    return (
      <div className="container">
      <div className="header">
        <button className="back-button" onClick={handleBack}>
        <FontAwesomeIcon icon={faArrowLeft} />
        <span>Voltar</span>
        </button>
        <h1>Resultado</h1>
      </div>

      <div className="result-content">
        {selectedImage && (
        <img 
          src={selectedImage} 
          alt="Equipamento identificado" 
          className="result-image"
        />
        )}
        <div className="result-text">
        {isProcessing ? (
          <p className="processing">Analisando equipamento</p>
        ) : (
          <>
          <h2>Equipamentos identificados:</h2>
            {backendResponse && backendResponse.similarity_results && backendResponse.similarity_results.map((item, index) => (
              <div key={item.id} className="equipment-item">
                {/* Cabeçalho clicável */}
                <div 
                  className="equipment-header"
                  onClick={() => toggleExpand(item.id)}
                >
                  <h3>{index + 1} - {item.payload.equipamento.charAt(0).toUpperCase() + item.payload.equipamento.slice(1)} - Similaridade: {item.score}%</h3>
                  <span className="expand-icon">
                    <FontAwesomeIcon icon={expandedItems[item.id] ? faChevronUp : faChevronDown} />
                  </span>
                </div>
                
                {/* Imagem do equipamento (sempre visível abaixo do header) */}
                {item.payload.image_path && (
                  <div className="equipment-image-container">
                    <img 
                      src={item.payload.image_path} 
                      alt={item.payload.equipamento} 
                      className="equipment-image"
                    />
                  </div>
                )}
                
                {/* Conteúdo expandível */}
                {expandedItems[item.id] && (
                  <div className="equipment-details">
                    <div className="detail-item">
                      <strong>Descrição:</strong> 
                      <div className="detail-text">{item.payload.descricao}</div>
                    </div>
                    <div className="detail-item">
                      <strong>Instruções:</strong> 
                      <div className="detail-text">{item.payload.instrucoes}</div>
                    </div>
                    <div className="detail-item">
                      <strong>Exemplo:</strong> 
                      <div className="detail-text">{item.payload.exemplo}</div>
                    </div>
                    {item.payload.observacoes && (
                      <div className="detail-item">
                        <strong>Observações:</strong> 
                        <div className="detail-text">{item.payload.observacoes}</div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </>
        )}
        </div>
      </div>
      </div>
    )
  }

  return (
    <div className="container">
      <h1>Descubra o equipamento</h1>
      
      <div className="instructions-section">
        <h2>Como usar:</h2>
        <ol>
          <li>Clique no botão "Enviar foto" abaixo</li>
          <li>Selecione uma foto clara do equipamento de laboratório</li>
          <li>Certifique-se de que não tenha outros equipamentos na imagem além do desejado</li>
          <li>Aguarde o processamento da imagem</li>
          <li>O resultado aparecerá com o nome do equipamento identificado</li>
        </ol>
      </div>
      
      <div className="upload-section">
        <label className="upload-button">
          Enviar foto
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            hidden
          />
        </label>
      </div>
    </div>
  )
}

export default App