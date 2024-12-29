// 存储键名
const STORAGE_KEYS = {
    AUDIO_BLOB: 'audioBlob',
    SEGMENTS: 'segments',
    RECORDING_STATE: 'recordingState'
};

// 全局变量
let mediaRecorder = null;
let audioChunks = [];
let currentAudioBlob = null;
let segments = [];

// DOM 元素
const elements = {
    startRecording: document.getElementById('startRecording'),
    stopRecording: document.getElementById('stopRecording'),
    clearData: document.getElementById('clearData'),
    addSegmentBtn: document.getElementById('addSegmentBtn'),
    submitBtn: document.getElementById('submitBtn'),
    audioPlayer: document.getElementById('audioPlayer'),
    audioElement: document.getElementById('audioElement'),
    segmentsContainer: document.querySelector('.segments-container'),
    status: document.getElementById('status'),
    languageSelect: document.getElementById('languageSelect'),
    modelSelect: document.getElementById('modelSelect')
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化按钮事件
    elements.startRecording.addEventListener('click', startRecording);
    elements.stopRecording.addEventListener('click', stopRecording);
    elements.clearData.addEventListener('click', clearAllData);
    elements.addSegmentBtn.addEventListener('click', addNewSegment);
    elements.submitBtn.addEventListener('click', submitTranscription);
    
    // 初始化片段容器事件委托
    elements.segmentsContainer.addEventListener('click', handleSegmentEvents);
    
    // 恢复保存的数据
    restoreState();
});

// 录音相关函数
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener('stop', () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            onRecordingComplete(audioBlob);
            stream.getTracks().forEach(track => track.stop());
        });

        mediaRecorder.start();
        elements.startRecording.style.display = 'none';
        elements.stopRecording.style.display = 'inline-block';
        showStatus('正在录音...', false, 'info');
    } catch (error) {
        console.error('Error starting recording:', error);
        showStatus('无法开始录音: ' + error.message, true, 'danger');
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        elements.startRecording.style.display = 'inline-block';
        elements.stopRecording.style.display = 'none';
        showStatus('录音已完成', false, 'success');
    }
}

// 音频处理函数
function updateAudioPlayer(blob) {
    if (blob) {
        const audioUrl = URL.createObjectURL(blob);
        elements.audioElement.src = audioUrl;
        elements.audioPlayer.style.display = 'block';
        currentAudioBlob = blob;
        saveState();
    } else {
        elements.audioPlayer.style.display = 'none';
        elements.audioElement.src = '';
    }
}

async function onRecordingComplete(blob) {
    updateAudioPlayer(blob);
    
    try {
        showStatus('正在处理音频...', false, 'info');
        const formData = new FormData();
        formData.append('audio', blob);
        formData.append('language', elements.languageSelect.value);
        formData.append('model', elements.modelSelect.value);

        const response = await fetch('/transcribe', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.error) {
            showStatus(result.error, true, 'danger');
        } else {
            displayTranscription(result);
            showStatus('转录完成！', false, 'success');
        }
    } catch (error) {
        console.error('Error processing audio:', error);
        showStatus('处理音频时出错: ' + error.message, true, 'danger');
    }
}

// 片段管理函数
function createSegmentElement(segment, index) {
    const segmentDiv = document.createElement('div');
    segmentDiv.className = 'segment';
    segmentDiv.dataset.index = index;

    segmentDiv.innerHTML = `
        <div class="segment-controls">
            <button class="btn btn-primary btn-sm play-segment-btn">
                <i class="fas fa-play"></i> 播放片段
            </button>
            <button class="btn btn-info btn-sm edit-time-btn">
                <i class="fas fa-clock"></i> 调整时间
            </button>
            <button class="btn btn-danger btn-sm delete-segment-btn">
                <i class="fas fa-trash"></i> 删除片段
            </button>
        </div>
        <div class="time-controls">
            <div class="row">
                <div class="col-md-6">
                    <label>开始时间 (秒):</label>
                    <input type="number" class="form-control start-time" 
                           value="${segment.start}" step="0.1" min="0">
                </div>
                <div class="col-md-6">
                    <label>结束时间 (秒):</label>
                    <input type="number" class="form-control end-time" 
                           value="${segment.end}" step="0.1" min="0">
                </div>
            </div>
        </div>
        <textarea class="form-control segment-text" rows="2">${segment.text || ''}</textarea>
    `;

    return segmentDiv;
}

function handleSegmentEvents(e) {
    const target = e.target;
    const segmentDiv = target.closest('.segment');
    if (!segmentDiv) return;

    if (target.classList.contains('play-segment-btn')) {
        playSegment(segmentDiv);
    } else if (target.classList.contains('delete-segment-btn')) {
        deleteSegment(segmentDiv);
    } else if (target.classList.contains('edit-time-btn')) {
        toggleTimeControls(segmentDiv);
    }
}

function playSegment(segmentDiv) {
    const index = parseInt(segmentDiv.dataset.index);
    const segment = segments[index];
    if (segment && elements.audioElement) {
        elements.audioElement.currentTime = segment.start;
        elements.audioElement.play();
        setTimeout(() => {
            elements.audioElement.pause();
        }, (segment.end - segment.start) * 1000);
    }
}

function deleteSegment(segmentDiv) {
    const index = parseInt(segmentDiv.dataset.index);
    segments.splice(index, 1);
    updateSegmentData();
}

function addNewSegment() {
    const newSegment = {
        start: 0,
        end: elements.audioElement.duration || 0,
        text: ''
    };
    segments.push(newSegment);
    updateSegmentData();
}

// 数据管理函数
function updateSegmentData() {
    segments.sort((a, b) => a.start - b.start);
    elements.segmentsContainer.innerHTML = '';
    segments.forEach((segment, index) => {
        const segmentElement = createSegmentElement(segment, index);
        elements.segmentsContainer.appendChild(segmentElement);
    });
    saveState();
}

function saveState() {
    try {
        if (currentAudioBlob) {
            const reader = new FileReader();
            reader.readAsDataURL(currentAudioBlob);
            reader.onloadend = function() {
                localStorage.setItem(STORAGE_KEYS.AUDIO_BLOB, reader.result);
            };
        }
        
        if (segments.length > 0) {
            localStorage.setItem(STORAGE_KEYS.SEGMENTS, JSON.stringify(segments));
        }
        
        localStorage.setItem(STORAGE_KEYS.RECORDING_STATE, JSON.stringify({
            isRecording: mediaRecorder?.state === 'recording',
            timestamp: new Date().getTime()
        }));
    } catch (error) {
        console.error('Error saving state:', error);
        showStatus('自动保存失败', true, 'warning');
    }
}

async function restoreState() {
    try {
        const audioData = localStorage.getItem(STORAGE_KEYS.AUDIO_BLOB);
        if (audioData) {
            const response = await fetch(audioData);
            currentAudioBlob = await response.blob();
            updateAudioPlayer(currentAudioBlob);
        }
        
        const segmentsData = localStorage.getItem(STORAGE_KEYS.SEGMENTS);
        if (segmentsData) {
            segments = JSON.parse(segmentsData);
            updateSegmentData();
        }
        
        const recordingState = localStorage.getItem(STORAGE_KEYS.RECORDING_STATE);
        if (recordingState) {
            const state = JSON.parse(recordingState);
            const timePassed = new Date().getTime() - state.timestamp;
            if (state.isRecording && timePassed < 5 * 60 * 1000) {
                showStatus('检测到上次录音可能未正常结束，建议清除数据重新开始', true, 'warning');
            }
        }
    } catch (error) {
        console.error('Error restoring state:', error);
        showStatus('恢复保存的数据失败', true, 'danger');
    }
}

function clearAllData() {
    if (confirm('确定要清除所有数据吗？这将删除当前的录音和转录内容。')) {
        try {
            if (mediaRecorder?.state === 'recording') {
                mediaRecorder.stop();
            }
            
            Object.values(STORAGE_KEYS).forEach(key => {
                localStorage.removeItem(key);
            });
            
            currentAudioBlob = null;
            segments = [];
            audioChunks = [];
            
            updateAudioPlayer(null);
            updateSegmentData();
            
            elements.startRecording.style.display = 'inline-block';
            elements.stopRecording.style.display = 'none';
            
            showStatus('所有数据已清除', false, 'success');
        } catch (error) {
            console.error('Error clearing data:', error);
            showStatus('清除数据失败', true, 'danger');
        }
    }
}

// 工具函数
function showStatus(message, isError = false, type = 'info') {
    elements.status.textContent = message;
    elements.status.style.display = 'block';
    elements.status.className = `alert alert-${type}`;
    
    if (!isError) {
        setTimeout(() => {
            elements.status.style.display = 'none';
        }, 3000);
    }
}

// 提交功能
async function submitTranscription() {
    try {
        const response = await fetch('/save-annotation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                segments: segments.map(segment => ({
                    start: segment.start,
                    end: segment.end,
                    text: segment.text
                }))
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus('标注已保存！', false, 'success');
        } else {
            showStatus(result.error || '保存失败', true, 'danger');
        }
    } catch (error) {
        console.error('Error submitting transcription:', error);
        showStatus('保存标注时出错: ' + error.message, true, 'danger');
    }
}

function displayTranscription(result) {
    segments = result.segments;
    updateSegmentData();
    showStatus('转录完成！', false, 'success');
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    seconds = Math.floor(seconds % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

function toggleTimeControls(segmentDiv) {
    const timeControls = segmentDiv.querySelector('.time-controls');
    timeControls.style.display = timeControls.style.display === 'none' ? 'block' : 'none';
}

function playPauseButton() {
    if (elements.audioElement.paused) {
        elements.audioElement.play();
        elements.playPauseButton.textContent = '暂停';
    } else {
        elements.audioElement.pause();
        elements.playPauseButton.textContent = '播放';
    }
}

async function submitToServer(audioData, transcription) {
    try {
        const formData = new FormData();
        formData.append('audio', audioData);
        formData.append('language', document.getElementById('languageSelect').value);
        formData.append('model', document.getElementById('modelSelect').value);

        const response = await fetch('/api/transcribe', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Transcription failed');
        }

        const result = await response.json();
        
        // Submit to Codatta if we have an active session
        await submitToCodatta(audioData, result.transcription);
        
        return result;
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process audio: ' + error.message);
    }
}

async function submitToCodatta(audioData, transcription) {
    try {
        const response = await fetch('/api/submit_annotation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                audio_data: audioData,
                transcription: transcription,
                language: document.getElementById('languageSelect').value,
                model: document.getElementById('modelSelect').value
            })
        });

        if (!response.ok) {
            if (response.status === 401) {
                console.log('No active Codatta session, skipping submission');
                return;
            }
            throw new Error('Failed to submit to Codatta');
        }

        const result = await response.json();
        console.log('Successfully submitted to Codatta:', result);
    } catch (error) {
        console.error('Error submitting to Codatta:', error);
        // Don't alert the user, just log the error
    }
}
