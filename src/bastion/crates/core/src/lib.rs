src/bastion/crates/core/src/lib.rs

// ============================================================================
// SECURITY CONTROL PANE - CORE MODULES (BASTION INTERFACE)
// ============================================================================

//! Core contract for Bastion Hosts to communicate with external systems,
//! managing state transitions between client requests and server responses.
//! Implements a robust abstraction layer using Rust's standard library features where possible.

use std::sync::{Arc, Mutex};
use std::time::Duration;
use crate::error::*;
use crate::firecracker::{FirecrackerAdapter, FirecrackerConfig, VmInstance, VmState};
use crate::forced_command::ForcedCommandConfig;
use crate::network_guard::NetworkGuard;
use crate::policy::{PolicyDecision, PolicyEngine, Policies};

/// Abstract interface for all supported communication protocols.
pub trait BastionInterface {
    /// The type of protocol this host implements (e.g., `AsyncProtocolExecutor`, `MessageHandler`).
    const PROTOCOL: &'static str;

    /// Configuration constants specific to the protocol implementation.
    fn CONFIG(&self) -> FirecrackerConfig;

    /// Execute a command or action as defined by the policy engine, respecting security constraints.
    async fn execute_command(
        self: Self::PROTOCOL,
        config: &ForcedCommandConfig,
        policies: Policies<Self>,
    ) -> Result<PolicyDecision>;

    /// Handle incoming messages from external clients using the specified protocol.
    fn handle_messages(&self) -> std::sync::{Arc<Mutex<Vec<Message>>>, Arc<RwLock<std::collections::HashMap<String, String>>>>;
}

/// Implementation of an Async Protocol Executor. Handles asynchronous event loops and streaming data streams.
pub struct AsyncProtocolExecutor {
    config: FirecrackerConfig,
    state: VmState,
    active_sessions: Vec<Session>, // Stores (session_id, timeout_ms) tuples for cleanup tracking
}

impl BastionInterface for AsyncProtocolExecutor {
    const PROTOCOL: &'static str = "Async";

    fn CONFIG(&self) -> FirecrackerConfig {
        self.config.clone()
    }

    async fn execute_command(
        &self,
        config: ForcedCommandConfig,
        policies: Policies<Self>,
    ) -> Result<PolicyDecision> {
        // In a real implementation, this would dispatch to an event loop or use the provided executor.
        // Here we simulate the command execution phase by returning a success decision with context.
        Ok(PolicyDecision::Success(config))
    }

    fn handle_messages(&self) -> std::sync::{Arc<Mutex<Vec<Message>>>, Arc<RwLock<std::collections::HashMap<String, String>>>> {
        let mut messages = self.state.lock().unwrap();
        // Simulate receiving incoming client requests. In production: use a server-side listener or WebSocket handling here.
        if let Some(msg) = messages.get_mut() {
            *msg.push(Message::Incoming("client_request".to_string()));
        }

        Arc::new(Mutex::new(messages))
    }
}

/// Implementation of a Message Handler for synchronous batched message processing (e.g., CLI or REST API).
pub struct MessageHandler;

impl BastionInterface for MessageHandler {
    const PROTOCOL: &'static str = "Sync";

    fn CONFIG(&self) -> FirecrackerConfig {
        // Simplified config placeholder. In production, use the actual protocol-specific constants.
        let mut cfg = FirecrackerConfig::default();
        cfg.default_timeout_ms = 30_000; // Default timeout for batched processing in ms
        cfg.max_batch_size = 1000;       // Max messages per message handler to avoid blocking
        cfg.retry_on_failure = true;     // Retry logic could be implemented here if needed

        cfg.clone()
    }

    async fn execute_command(
        &self,
        config: ForcedCommandConfig,
        policies: Policies<Self>,
    ) -> Result<PolicyDecision> {
        Ok(PolicyDecision::Success(config))
    }

    // Helper to handle incoming messages synchronously.
    fn handle_messages(&self) -> std::sync::{Arc<Mutex<Vec<Message>>>, Arc<RwLock<std::collections::HashMap<String, String>>>> {
        let mut messages = self.state.lock().unwrap();
        
        if let Some(msgs) = messages.get_mut() {
            // Process incoming client requests immediately.
            for &msg in msgs.iter_mut() {
                *msg.push(Message::Incoming("client_request".to_string()));
            }

            // Simulate processing batched data (e.g., sending responses to clients).
            if let Some(msgs) = messages.get
