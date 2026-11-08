# Deep Learning Architectures and Training: PyTorch, U-Net Segmentation, ResNet/ViT, AdamW and AMP

**Category**: `deep_learning_core` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Deep Learning Architecture Selection (Project/U_net_ and CV): (1) Image Classification: ResNet50 (residual skip connections y = F(x) + x prevent vanishing gradients) or Vision Transformer (ViT). (2) Pixel-Level Semantic Segmentation (Medical/Industrial Microscopy): U-Net symmetric Encoder-Decoder with skip connections concatenating high-resolution encoder feature maps with upsampled decoder maps, trained with Dice Loss + Binary Cross-Entropy (BCE). (3) PyTorch Production Training Loop: optimizer.zero_grad(set_to_none=True) -> torch.amp.autocast(bf16/fp16) forward pass -> loss.backward() -> clip_grad_norm_ -> optimizer.step() with AdamW (decoupled weight decay) and Cosine Annealing LR with Warmup.

## Connected GraphRAG Entities

- `Deep_Learning_PyTorch_UNet`
- `CNN_ResNet50_Project`
