use anchor_lang::prelude::*;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod talos_vault {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        vault.owner = ctx.accounts.signer.key();
        vault.balance = 0;
        
        emit!(VaultInitialized {
            owner: vault.owner,
            timestamp: Clock::get()?.unix_timestamp,
        });
        
        Ok(())
    }

    pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        
        let ix = anchor_lang::solana_program::system_instruction::transfer(
            &ctx.accounts.signer.key(),
            &vault.key(),
            amount,
        );
        
        anchor_lang::solana_program::program::invoke(
            &ix,
            &[
                ctx.accounts.signer.to_account_info(),
                vault.to_account_info(),
                ctx.accounts.system_program.to_account_info(),
            ],
        )?;

        vault.balance = vault.balance.checked_add(amount).unwrap();
        
        emit!(LiquidityAdded {
            user: ctx.accounts.signer.key(),
            amount,
            new_balance: vault.balance,
        });

        Ok(())
    }

    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        
        require!(ctx.accounts.signer.key() == vault.owner, VaultError::Unauthorized);
        require!(vault.balance >= amount, VaultError::InsufficientFunds);

        **vault.to_account_info().try_borrow_mut_lamports()? -= amount;
        **ctx.accounts.signer.to_account_info().try_borrow_mut_lamports()? += amount;

        vault.balance = vault.balance.checked_sub(amount).unwrap();

        emit!(LiquidityRemoved {
            owner: ctx.accounts.signer.key(),
            amount,
            remaining_balance: vault.balance,
        });

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = signer,
        space = 8 + 32 + 8,
        seeds = [b"vault", signer.key().as_ref()],
        bump
    )]
    pub vault: Account<'info, VaultState>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(
        mut,
        seeds = [b"vault", signer.key().as_ref()],
        bump
    )]
    pub vault: Account<'info, VaultState>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(
        mut,
        seeds = [b"vault", signer.key().as_ref()],
        bump
    )]
    pub vault: Account<'info, VaultState>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct VaultState {
    pub owner: Pubkey,
    pub balance: u64,
}

#[error_code]
pub enum VaultError {
    #[msg("Unauthorized access denied.")]
    Unauthorized,
    #[msg("Insufficient liquidity in vault.")]
    InsufficientFunds,
}

// --- EVENTS ---
#[event]
pub struct VaultInitialized {
    pub owner: Pubkey,
    pub timestamp: i64,
}

#[event]
pub struct LiquidityAdded {
    pub user: Pubkey,
    pub amount: u64,
    pub new_balance: u64,
}

#[event]
pub struct LiquidityRemoved {
    pub owner: Pubkey,
    pub amount: u64,
    pub remaining_balance: u64,
}
