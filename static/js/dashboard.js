// F1 Racer AI Agent - Dashboard JavaScript with Comprehensive Feedback

// Speak functionality with detailed feedback
document.getElementById('speakForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = addLoadingState(button);
    
    showToast('Processing...', 'Generating F1 message with AI...', 'info', 2000);
    
    try {
        const formData = new FormData(this);
        const data = {
            message_type: formData.get('messageType'),
            custom_context: formData.get('customContext')
        };
        
        const result = await makeApiRequest('/speak', 'POST', data);
        
        if (result.success) {
            showResultCard('speakResult', 'Message Generated Successfully!', result.message, {
                'Message Type': data.message_type,
                'Custom Context': data.custom_context || 'None',
                'Generated At': formatTimestamp(result.timestamp)
            });
            
            showToast('Success!', `${data.message_type.charAt(0).toUpperCase() + data.message_type.slice(1)} message generated successfully!`, 'success');
        }
        
    } catch (error) {
        showToast('Generation Failed', `Error generating message: ${error.message}`, 'danger');
    } finally {
        removeLoadingState(button, originalText);
    }
});

// Post status functionality with engagement feedback
document.getElementById('postForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = addLoadingState(button);
    
    showToast('Posting...', 'Publishing your status update...', 'info', 2000);
    
    try {
        const formData = new FormData(this);
        const data = {
            content: formData.get('postContent')
        };
        
        const result = await makeApiRequest('/act/post', 'POST', data);
        
        if (result.success) {
            showResultCard('actResult', 'Status Posted Successfully!', result.content, {
                'Engagement': `${result.engagement} interactions`,
                'Posted At': formatTimestamp(result.timestamp),
                'Content Type': 'Status Update'
            });
            
            showToast('Posted!', `Status update published with ${result.engagement} predicted interactions!`, 'success');
            this.reset();
        }
        
    } catch (error) {
        showToast('Post Failed', `Error posting status: ${error.message}`, 'danger');
    } finally {
        removeLoadingState(button, originalText);
    }
});

// Reply to comment with sentiment analysis feedback
document.getElementById('replyForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!validateForm('replyForm')) return;
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = addLoadingState(button);
    
    showToast('Analyzing...', 'Analyzing fan comment sentiment and generating reply...', 'info', 2000);
    
    try {
        const fanComment = document.getElementById('fanComment').value;
        const data = {
            fan_comment: fanComment
        };
        
        const result = await makeApiRequest('/act/reply', 'POST', data);
        
        if (result.success) {
            showResultCard('actResult', 'Reply Posted Successfully!', 
                `<strong>Original:</strong> "${result.original_comment}"<br><br><strong>Your Reply:</strong> "${result.reply}"`,
                {
                    'Comment Sentiment': result.sentiment.charAt(0).toUpperCase() + result.sentiment.slice(1),
                    'Reply Type': 'Fan Interaction',
                    'Posted At': formatTimestamp(result.timestamp)
                }
            );
            
            const sentimentEmoji = result.sentiment === 'positive' ? '😊' : result.sentiment === 'negative' ? '😔' : '😐';
            showToast('Reply Sent!', `Reply posted to ${result.sentiment} comment ${sentimentEmoji}`, 'success');
            this.reset();
        }
        
    } catch (error) {
        showToast('Reply Failed', `Error replying to comment: ${error.message}`, 'danger');
    } finally {
        removeLoadingState(button, originalText);
    }
});

// Like post functionality with confirmation
document.getElementById('likeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!validateForm('likeForm')) return;
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = addLoadingState(button);
    
    showToast('Liking...', 'Processing post like action...', 'info', 1000);
    
    try {
        const postContent = document.getElementById('likeContent').value;
        const data = {
            post_content: postContent
        };
        
        const result = await makeApiRequest('/act/like', 'POST', data);
        
        if (result.success) {
            showResultCard('actResult', 'Post Liked Successfully!', 
                `Post liked: "${result.liked_post}"`,
                {
                    'Action Type': 'Social Media Engagement',
                    'Liked At': formatTimestamp(result.timestamp)
                }
            );
            
            showToast('Liked! ❤️', 'Post liked successfully!', 'success');
            this.reset();
        }
        
    } catch (error) {
        showToast('Like Failed', `Error liking post: ${error.message}`, 'danger');
    } finally {
        removeLoadingState(button, originalText);
    }
});

// Mention someone with context awareness
document.getElementById('mentionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!validateForm('mentionForm')) return;
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = addLoadingState(button);
    
    showToast('Creating Mention...', 'Generating contextual mention post...', 'info', 2000);
    
    try {
        const personName = document.getElementById('personName').value;
        const mentionContext = document.getElementById('mentionContext').value;
        const data = {
            person_name: personName,
            context: mentionContext
        };
        
        const result = await makeApiRequest('/act/mention', 'POST', data);
        
        if (result.success) {
            showResultCard('actResult', 'Mention Posted Successfully!', result.content, {
                'Mentioned Person': `@${result.mentioned_person}`,
                'Context': result.context.charAt(0).toUpperCase() + result.context.slice(1),
                'Posted At': formatTimestamp(result.timestamp)
            });
            
            showToast('Mentioned!', `@${result.mentioned_person} mentioned in ${result.context} context`, 'success');
            this.reset();
        }
        
    } catch (error) {
        showToast('Mention Failed', `Error creating mention: ${error.message}`, 'danger');
    } finally {
        removeLoadingState(button, originalText);
    }
});

// Load context with detailed display and sidebar update
async function loadContext() {
    showToast('Loading...', 'Fetching current agent context...', 'info', 1000);
    
    try {
        const result = await makeApiRequest('/think/context');
        
        if (result.success) {
            displayContext(result.context);
            updateSidebarContext(result.context);
            showToast('Context Loaded!', 'Agent context refreshed successfully', 'success', 2000);
        }
        
    } catch (error) {
        showToast('Load Failed', `Error loading context: ${error.message}`, 'danger');
    }
}

// Update context with detailed feedback
document.getElementById('updateForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = addLoadingState(button);
    
    showToast('Updating...', 'Updating agent context...', 'info', 2000);
    
    try {
        const formData = new FormData(this);
        const data = {
            circuit: formData.get('circuit'),
            session: formData.get('session'),
            mood: formData.get('mood')
        };
        
        // Remove empty values
        Object.keys(data).forEach(key => {
            if (!data[key]) delete data[key];
        });
        
        if (Object.keys(data).length === 0) {
            showToast('No Changes', 'Please select at least one field to update', 'warning');
            removeLoadingState(button, originalText);
            return;
        }
        
        const result = await makeApiRequest('/think/update', 'POST', data);
        
        if (result.success) {
            const updateList = Object.entries(result.updates)
                .map(([key, value]) => `${key.replace('_', ' ')}: ${value}`)
                .join(', ');
            
            showResultCard('thinkResult', 'Context Updated Successfully!', 
                `Updated fields: ${updateList}`,
                {
                    'Update Time': new Date().toLocaleString(),
                    'Fields Changed': Object.keys(result.updates).length
                }
            );
            
            // Refresh context display and sidebar
            loadContext();
            
            showToast('Updated!', `Context updated: ${updateList}`, 'success');
            this.reset();
        }
        
    } catch (error) {
        showToast('Update Failed', `Error updating context: ${error.message}`, 'danger');
    } finally {
        removeLoadingState(button, originalText);
    }
});

// Race simulation with progress feedback
document.getElementById('simulationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = addLoadingState(button);
    
    const simulationLoading = document.getElementById('simulationLoading');
    simulationLoading.classList.remove('f1-hidden');
    
    showToast('Starting Simulation...', 'Preparing race weekend simulation...', 'info', 2000);
    
    try {
        const formData = new FormData(this);
        const data = {
            circuit_key: formData.get('circuit_key'),
            weekend_type: formData.get('weekend_type')
        };
        
        showToast('Simulating...', `Running ${data.weekend_type.replace('_', ' ')} simulation...`, 'info', 3000);
        
        const result = await makeApiRequest('/simulation', 'POST', data);
        
        if (result.success) {
            displaySimulationResults(result.results);
            document.getElementById('simulationResult').classList.remove('f1-hidden');
            
            const finalPos = result.results.sessions[result.results.sessions.length - 1].result.position;
            const positionText = finalPos <= 3 ? `podium finish (P${finalPos})! 🏆` : 
                                finalPos <= 10 ? `points finish (P${finalPos})` : 
                                `P${finalPos} finish`;
            
            showToast('Simulation Complete!', `Race weekend finished with ${positionText}`, 'success');
        }
        
    } catch (error) {
        showToast('Simulation Failed', `Error running simulation: ${error.message}`, 'danger');
    } finally {
        removeLoadingState(button, originalText);
        simulationLoading.classList.add('f1-hidden');
    }
});

// Helper function to show result cards
function showResultCard(containerId, title, content, metadata = {}) {
    const container = document.getElementById(containerId);
    
    const metadataHtml = Object.keys(metadata).length > 0 ? 
        `<div class="f1-result-meta">
            ${Object.entries(metadata).map(([key, value]) => 
                `<strong>${key}:</strong> ${value}`
            ).join(' • ')}
        </div>` : '';
    
    container.innerHTML = `
        <div class="f1-result">
            <div class="f1-result-header">
                <i class="f1-result-icon fas fa-check-circle"></i>
                <h3 class="f1-result-title">${title}</h3>
            </div>
            <div class="f1-result-content">${content}</div>
            ${metadataHtml}
            <button class="f1-copy-btn" onclick="copyToClipboard('${content.replace(/<[^>]*>/g, '')}', 'Result copied to clipboard!')">
                <i class="fas fa-copy"></i> Copy Result
            </button>
        </div>
    `;
    
    container.classList.remove('f1-hidden');
}

// Display context information with enhanced formatting
function displayContext(context) {
    const contextDisplay = document.getElementById('contextDisplay');
    
    const sections = [
        {
            title: 'Driver Information',
            data: context.driver_info,
            color: 'var(--f1-red)'
        },
        {
            title: 'Current Situation', 
            data: context.current_situation,
            color: 'var(--info)'
        },
        {
            title: 'Recent Activity',
            data: context.recent_activity,
            color: 'var(--warning)'
        },
        {
            title: 'Circuit Details',
            data: context.circuit_details,
            color: 'var(--success)'
        }
    ];
    
    const html = sections.map(section => `
        <div class="f1-context-section">
            <div class="f1-context-title" style="color: ${section.color};">${section.title}</div>
            ${Object.entries(section.data).map(([key, value]) => {
                if (key === 'last_result' && value) {
                    return `<div class="f1-context-item">
                        <span class="f1-context-label">Last Result</span>
                        <span class="f1-context-value">P${value.position} - ${value.best_time}</span>
                    </div>`;
                } else if (key === 'recent_incidents' && Array.isArray(value) && value.length > 0) {
                    return `<div class="f1-context-item">
                        <span class="f1-context-label">Recent Incidents</span>
                        <span class="f1-context-value">${value.join(', ')}</span>
                    </div>`;
                } else if (key === 'characteristics' && Array.isArray(value)) {
                    return `<div class="f1-context-item">
                        <span class="f1-context-label">Characteristics</span>
                        <span class="f1-context-value">${value.map(c => 
                            `<span style="background: var(--f1-grey); padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.8rem; margin-right: 0.3rem;">${c}</span>`
                        ).join('')}</span>
                    </div>`;
                } else if (value && typeof value !== 'object') {
                    return `<div class="f1-context-item">
                        <span class="f1-context-label">${key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        <span class="f1-context-value">${value}</span>
                    </div>`;
                }
                return '';
            }).join('')}
        </div>
    `).join('');
    
    contextDisplay.innerHTML = html;
}

// Update sidebar context information
function updateSidebarContext(context) {
    document.getElementById('currentCircuit').textContent = 
        context.current_situation.circuit || 'Not Set';
    document.getElementById('currentSession').textContent = 
        context.current_situation.session || 'None';
    document.getElementById('currentMood').textContent = 
        context.current_situation.mood || 'Neutral';
}

// Display simulation results with enhanced formatting
function displaySimulationResults(results) {
    const container = document.getElementById('simulationResult');
    
    const html = `
        <div class="f1-result">
            <div class="f1-result-header">
                <i class="f1-result-icon fas fa-flag-checkered"></i>
                <h3 class="f1-result-title">Race Weekend Simulation Complete!</h3>
            </div>
            
            <div class="f1-result-content">
                <div style="text-align: center; margin-bottom: 2rem;">
                    <h4 style="color: var(--f1-red); font-family: 'Orbitron', monospace;">
                        ${results.circuit} - ${results.weekend_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </h4>
                </div>
                
                <div class="f1-race-results">
                    ${results.sessions.map(session => `
                        <div class="f1-session-result">
                            <div class="f1-session-header">
                                <div class="f1-session-title">
                                    ${session.day} - ${formatSessionType(session.session)}
                                </div>
                                ${formatPosition(session.result.position)}
                            </div>
                            <div style="margin: 1rem 0; font-size: 0.9rem; color: var(--f1-light-grey);">
                                <strong>Best Time:</strong> ${session.result.best_time} • 
                                <strong>Laps:</strong> ${session.result.laps_completed}
                            </div>
                            <div class="f1-session-message">
                                "${session.message}"
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; background: var(--f1-grey); border-radius: 10px; border-left: 4px solid var(--success);">
                    <h4 style="color: var(--success); margin-bottom: 1rem;">Weekend Summary</h4>
                    <p style="font-size: 1.1rem; color: var(--f1-white);">${results.final_status}</p>
                </div>
            </div>
            
            <div class="f1-result-meta">
                <strong>Sessions Completed:</strong> ${results.sessions.length} • 
                <strong>Weekend Type:</strong> ${results.weekend_type.replace('_', ' ')} • 
                <strong>Circuit:</strong> ${results.circuit}
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

// Initialize dashboard with context loading
document.addEventListener('DOMContentLoaded', function() {
    // Load initial context
    setTimeout(() => {
        loadContext();
    }, 1000);
    
    showToast('Dashboard Ready!', 'F1 AI Agent dashboard loaded. Ready to start racing! 🏎️', 'success', 3000);
});